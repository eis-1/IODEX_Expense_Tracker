"""
Backup module for automated database backups.
Supports creating, managing, and restoring database backups.
"""
import shutil
import os
import sqlite3
from datetime import datetime, timedelta
from typing import List, Tuple


class BackupManager:
    """Manages automated backups of the expense database."""
    
    def __init__(self, db_path: str = "expenses.db", backup_dir: str = ".backups"):
        """
        Initialize backup manager.
        
        Args:
            db_path: Path to the main database file
            backup_dir: Directory to store backups
        """
        self.db_path = db_path
        self.backup_dir = backup_dir
        
        # Create backup directory if it doesn't exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
    
    def create_backup(self, description: str = "") -> str:
        """
        Create a backup of the database.
        
        Args:
            description: Optional description for the backup
            
        Returns:
            Path to the backup file
            
        Raises:
            IOError: If backup cannot be created
        """
        if not os.path.exists(self.db_path):
            raise IOError(f"Database file not found: {self.db_path}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup_name = f"expenses_backup_{timestamp}.db"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        # Use SQLite backup API for consistent backups
        try:
            source_conn = sqlite3.connect(self.db_path)
            backup_conn = sqlite3.connect(backup_path)
            try:
                source_conn.backup(backup_conn)
            finally:
                source_conn.close()
                backup_conn.close()
            
            # Write metadata file
            if description:
                metadata_path = backup_path + ".meta"
                with open(metadata_path, 'w') as f:
                    f.write(f"Created: {datetime.now().isoformat()}\n")
                    f.write(f"Description: {description}\n")
                    f.write(f"Original DB: {self.db_path}\n")
            
            return backup_path
        
        except Exception as e:
            # Clean up incomplete backup
            if os.path.exists(backup_path):
                os.remove(backup_path)
            raise IOError(f"Failed to create backup: {str(e)}")
    
    def list_backups(self) -> List[Tuple[str, str, int, str]]:
        """
        List all available backups.
        
        Returns:
            List of tuples: (backup_path, timestamp, file_size, description)
        """
        backups = []
        
        if not os.path.exists(self.backup_dir):
            return backups
        
        for filename in sorted(os.listdir(self.backup_dir), reverse=True):
            if filename.endswith('.db'):
                backup_path = os.path.join(self.backup_dir, filename)
                file_size = os.path.getsize(backup_path)
                
                # Extract timestamp from filename
                # Format: expenses_backup_YYYYMMDD_HHMMSS.db
                timestamp = filename.replace('expenses_backup_', '').replace('.db', '')
                
                # Read description from metadata
                description = ""
                metadata_path = backup_path + ".meta"
                if os.path.exists(metadata_path):
                    try:
                        with open(metadata_path, 'r') as f:
                            for line in f:
                                if line.startswith('Description:'):
                                    description = line.replace('Description:', '').strip()
                                    break
                    except:
                        pass
                
                backups.append((backup_path, timestamp, file_size, description))
        
        return backups
    
    def restore_backup(self, backup_path: str) -> None:
        """
        Restore database from a backup.
        
        Args:
            backup_path: Path to the backup file to restore
            
        Raises:
            IOError: If restore fails
        """
        if not os.path.exists(backup_path):
            raise IOError(f"Backup file not found: {backup_path}")
        
        try:
            # Create a safety backup before restoring
            safety_backup = self.create_backup("Safety backup before restore")
            
            # Ensure any open connections are closed before restoring
            try:
                conn = sqlite3.connect(self.db_path)
                conn.close()
            except Exception:
                pass

            # Restore from backup using SQLite backup API
            backup_conn = sqlite3.connect(backup_path)
            target_conn = sqlite3.connect(self.db_path)
            try:
                backup_conn.backup(target_conn)
            finally:
                backup_conn.close()
                target_conn.close()
        
        except Exception as e:
            raise IOError(f"Failed to restore backup: {str(e)}")
    
    def delete_backup(self, backup_path: str) -> bool:
        """
        Delete a specific backup.
        
        Args:
            backup_path: Path to backup to delete
            
        Returns:
            True if deleted, False if not found
        """
        if not os.path.exists(backup_path):
            return False
        
        try:
            os.remove(backup_path)
            
            # Also remove metadata file if it exists
            metadata_path = backup_path + ".meta"
            if os.path.exists(metadata_path):
                os.remove(metadata_path)
            
            return True
        except:
            return False
    
    def cleanup_old_backups(self, days: int = 30, keep_minimum: int = 3) -> int:
        """
        Delete backups older than specified days, keeping at least keep_minimum recent backups.
        
        Args:
            days: Delete backups older than this many days
            keep_minimum: Minimum number of recent backups to keep
            
        Returns:
            Number of backups deleted
        """
        backups = self.list_backups()
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count = 0
        
        for i, (backup_path, timestamp, _, _) in enumerate(backups):
            # Keep minimum number of recent backups
            if i < keep_minimum:
                continue
            
            try:
                # Parse timestamp (format: YYYYMMDD_HHMMSS)
                backup_datetime = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                
                if backup_datetime < cutoff_date:
                    if self.delete_backup(backup_path):
                        deleted_count += 1
            except:
                continue
        
        return deleted_count
    
    def get_backup_info(self, backup_path: str) -> dict:
        """
        Get information about a specific backup.
        
        Args:
            backup_path: Path to backup file
            
        Returns:
            Dictionary with backup information
        """
        if not os.path.exists(backup_path):
            return {}
        
        try:
            file_size = os.path.getsize(backup_path)
            created_time = datetime.fromtimestamp(os.path.getctime(backup_path))
            
            # Count records in backup
            conn = sqlite3.connect(backup_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM expenses")
            record_count = cursor.fetchone()[0]
            conn.close()
            
            return {
                'path': backup_path,
                'size': file_size,
                'created': created_time.isoformat(),
                'record_count': record_count
            }
        except:
            return {'error': 'Could not read backup information'}
    
    def automatic_backup(self, description: str = "Automatic backup") -> str:
        """
        Create an automatic backup with cleanup of old backups.
        
        Args:
            description: Description for the backup
            
        Returns:
            Path to the created backup
        """
        # Create new backup
        backup_path = self.create_backup(description)
        
        # Clean up old backups (older than 30 days, keep at least 5)
        self.cleanup_old_backups(days=30, keep_minimum=5)
        
        return backup_path
