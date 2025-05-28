import shutil
from pathlib import Path

import git
from git import Repo

from app.config.setting import setting


class Commit:

    def __init__(self):
        self.repo_url = setting.GITHUB_REPO_URL_SAVE_FILES
        self.repo_name = self.repo_url.split("/")[-1].replace(".git", "")
        self.repo_path = Path("../repositories/" + self.repo_name)
        self.repo_url_with_token = self.repo_url.replace("https://", f"https://{setting.GITHUB_TOKEN}@")
        self.repo: Repo = self.__clone_repo()

    def write_file(self, file_name: str, text_to_write: str):
        folder_path = Path(str(self.repo_path) + '/strava/')
        full_file_path = folder_path.joinpath(file_name)

        folder_path.mkdir(parents=True, exist_ok=True)

        with open(full_file_path, "w") as f:
            f.write(text_to_write)

    def commit_and_push(self, commit_message: str) -> bool:
        try:
            self.repo.git.add(A=True)
            self.repo.git.config("user.name", "strava-map")
            self.repo.git.config("user.email", "comit@stravamap.com")
            self.repo.git.commit("-m", commit_message)
            self.repo.git.push("--set-upstream", self.repo_url_with_token, 'main')
            return True
        except Exception as e:
            print(f"Erro ao fazer commit/push: {e}")
            return False

    def __clone_repo(self) -> Repo:
        if self.repo_path.exists():
            self.__remove_repo_folder()

        return git.Repo.clone_from(self.repo_url_with_token, self.repo_path)

    def __remove_repo_folder(self):
        path = self.repo_path
        shutil.rmtree(path)
