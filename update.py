from tkinter import ttk, messagebox, scrolledtext, filedialog, Menu, simpledialog, Toplevel
import git
import subprocess

class AutoUpdater:
    def __init__(self, repo_path, pyinstaller_cmd, app):
        self.repo_path = repo_path
        self.pyinstaller_cmd = pyinstaller_cmd
        self.app = app

    def check_for_updates(self):
        print("Checking for updates...")  # Aggiunta della stampa
        repo = git.Repo(self.repo_path)
        repo.remotes.origin.pull()
        dirty = repo.is_dirty()
        print("Updates checked. Dirty:", dirty)
        return dirty

    def rebuild_app(self):
        print("Rebuilding the application...")
        subprocess.run(self.pyinstaller_cmd, shell=True)
        print("Application rebuilt.")

    def restart_app(self):
        print("Restarting the application...")
        self.app.on_exit()
        print("Application restarted.")

    def get_commit_messages(self):
        print("Getting commit messages...")
        repo = git.Repo(self.repo_path)
        origin = repo.remotes.origin
        origin.fetch()
        local_commits = list(repo.iter_commits('master..origin/master'))
        commit_messages = [commit.message.strip() for commit in local_commits]
        print("Commit messages retrieved:", commit_messages)
        return commit_messages

    def run(self):
        print("AutoUpdater started.")
        while True:
            if self.check_for_updates():
                print("Aggiornamenti disponibili.")  # Aggiunta della stampa
                updates_available = self.get_commit_messages()
                if updates_available:
                    message = "Sono disponibili aggiornamenti:\n\n" + "\n".join(updates_available)
                    if messagebox.askyesno("Aggiornamenti disponibili", message + "\n\nVuoi aggiornare l'applicazione?"):
                        self.rebuild_app()
                        self.restart_app()
                        messagebox.showinfo("Aggiornamento completato", "L'applicazione è stata aggiornata con successo.")
                    else:
                        messagebox.showinfo("Aggiornamenti ignorati", "L'applicazione non è stata aggiornata.")
                else:
                    print("Nessun aggiornamento disponibile.")  # Aggiunta della stampa
                    messagebox.showinfo("Nessun aggiornamento", "Non ci sono aggiornamenti disponibili.")
            else:
                messagebox.showinfo("Nessun aggiornamento", "Non ci sono aggiornamenti disponibili.")

