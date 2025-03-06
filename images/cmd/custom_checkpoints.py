from notebook.services.contents.filemanager import FileContentsManager
import os

class CentralizedCheckpoints(FileContentsManager):
    def create_checkpoint(self, path):
        # Define your custom checkpoint directory
        checkpoint_dir = '/opt/checkpoints'
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)

        # Generate a unique path for each notebook
        checkpoint_path = os.path.join(checkpoint_dir, path.replace('/', '_'))
        if not os.path.exists(os.path.dirname(checkpoint_path)):
            os.makedirs(os.path.dirname(checkpoint_path))

        # Save checkpoint
        return super().create_checkpoint(checkpoint_path)

    def delete_checkpoint(self, checkpoint_id, path):
        # Define custom deletion logic if needed
        return super().delete_checkpoint(checkpoint_id, path)

    def list_checkpoints(self, path):
        checkpoint_dir = '/opt/checkpoints'
        checkpoint_path = os.path.join(checkpoint_dir, path.replace('/', '_'))
        return super().list_checkpoints(checkpoint_path)
