import subprocess
import git
import time

class AutoUpdater:
    def __init__(self, repo_path, pyinstaller_cmd, app):
        self.repo_path = repo_path
        self.pyinstaller_cmd = pyinstaller_cmd
        self.app = app

    def check_for_updates(self):
        repo = git.Repo(self.repo_path)
        repo.remotes.origin.pull()
        return repo.is_dirty()

    def rebuild_app(self):
        subprocess.run(self.pyinstaller_cmd, shell=True)

    def restart_app(self):
        self.app.on_exit()

    def get_commit_messages(self):
        repo = git.Repo(self.repo_path)
        origin = repo.remotes.origin
        origin.fetch()
        local_commits = list(repo.iter_commits('master..origin/master'))
        commit_messages = [commit.message.strip() for commit in local_commits]
        return commit_messages

    def run(self):
        while True:
            if self.check_for_updates():
                print("Aggiornamenti rilevati, ricostruzione dell'app...")
                self.rebuild_app()
                self.restart_app()
                print("Applicazione riavviata con successo.")
            else:
                print("Nessun aggiornamento rilevato.")
            time.sleep(300)  # Esempio: controlla ogni 5 minuti

