# Tutoriel : Installer Python, pyenv et créer des environnements virtuels (Windows, macOS, Linux)

# 🧩 Introduction
Ce tutoriel vous apprendra à :

- Installer Python

- Installer pyenv pour gérer plusieurs versions de Python facilement

- Utiliser venv pour créer des environnements virtuels propres

- Basculer entre plusieurs versions de Python

- Travailler proprement sur vos projets Python sans "casser" votre machine

## 1. Pré-requis

- Savoir ouvrir un terminal (Windows Powershell / Terminal macOS / Terminal Linux)

- Savoir copier-coller des commandes

Pas besoin d'autres compétences particulières !

## 2. Tutoriel pour Windows
### 2.1. Installer Python via pyenv-win
Windows a une version spéciale de pyenv appelée pyenv-win.

Installer Git pour Windows (si ce n’est pas déjà fait) :

Télécharger : https://git-scm.com/download/win

Laisser toutes les options par défaut lors de l'installation.

Installer pyenv-win :

```Powershell
# Ouvrez PowerShell en mode Administrateur
Invoke-WebRequest -UseBasicParsing -Uri "https://pyenv.run" -OutFile "./pyenv-installer.ps1"
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\pyenv-installer.ps1
```

Puis, ajoutez ces lignes à votre variable d’environnement (manuel ou automatique, si vous ne savez pas comment faire voici un lien [Lien env vars](https://letmegooglethat.com/?q=comment+ajouter+des+variables+d%27environnement+sur+windows11)) :

Chemins à ajouter :

`%USERPROFILE%\.pyenv\pyenv-win\bin`

`%USERPROFILE%\.pyenv\pyenv-win\shims`

Vérifiez l’installation :

```Powershell
pyenv --version
Si une version s'affiche, c’est bon !
```

### 2.2. Installer une version spécifique de Python

```powershell
# Voir toutes les versions disponibles
pyenv install --list

# Installer par exemple Python 3.11.3
pyenv install 3.11.3

# Définir la version par défaut
pyenv global 3.11.3

# Vérifiez
python --version
```

### 2.3. Créer un environnement virtuel (venv)

```powershell
# Aller dans le dossier du projet
cd mon_projet/

# Créer un environnement virtuel
python -m venv env

# Activer l'environnement
.\env\Scripts\Activate

# Pour désactiver :
deactivate
```

## 3. Tutoriel pour macOS
### 3.1. Installer Homebrew (si ce n’est pas déjà fait)
Homebrew est indispensable sur Mac pour installer proprement des outils.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 3.2. Installer pyenv

```bash
brew update
brew install pyenv
```

Ajoutez pyenv au terminal :

```bash
# Ajoutez ceci à la fin du fichier ~/.bashrc (ou ~/.bash_profile, ~/.zshrc selon votre shell)

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Rechargez votre terminal
source ~/.bashrc
```

Vérifiez l'installation :

```bash
pyenv --version
```

### 3.3. Installer une version spécifique de Python
```bash
# Voir toutes les versions disponibles
pyenv install --list

# Installer par exemple Python 3.11.3
pyenv install 3.11.3

# Définir la version par défaut
pyenv global 3.11.3

# Vérifiez
python --version
```

### 3.4. Créer un environnement virtuel (venv)

```bash
# Aller dans le dossier du projet
cd mon_projet/

# Créer un environnement virtuel
python -m venv env

# Activer l'environnement
source env/bin/activate

# Pour désactiver :
deactivate
```

## 4. Tutoriel pour Linux (Ubuntu/Debian)
### 4.1. Installer les dépendances de build

```bash
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev git
```

### 4.2. Installer pyenv

```bash
curl https://pyenv.run | bash
```

Ajoutez pyenv à votre terminal :

```bash
# Ajoutez ceci à la fin du fichier ~/.bashrc (ou ~/.zshrc si vous utilisez zsh)

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Rechargez votre terminal
source ~/.bashrc
```

Vérifiez l'installation :

```bash
pyenv --version
```

### 4.3. Installer une version spécifique de Python

```bash
# Voir toutes les versions disponibles
pyenv install --list

# Installer par exemple Python 3.11.3
pyenv install 3.11.3

# Définir la version par défaut
pyenv global 3.11.3

# Vérifiez
python --version
```

### 4.4. Créer un environnement virtuel (venv)

```bash
# Aller dans le dossier du projet
cd mon_projet/

# Créer un environnement virtuel
python -m venv env

# Activer l'environnement
source env/bin/activate

# Pour désactiver :
deactivate
```

## 5. Résumé rapide 🧠

|Commande|Explication|
|--------|-----------|
|pyenv install X.X.X|Installer une version spécifique de Python|
|pyenv global X.X.X|Changer de version de Python globalement|
|python -m venv env|Créer un environnement virtuel|
|source env/bin/activate|Activer un environnement virtuel (Linux/macOS)|
|.\env\Scripts\Activate|Activer un environnement virtuel (Windows)|
|deactivate|Désactiver un environnement virtuelTutoriel : Installer Python, pyenv et créer des environnements virtuels (Windows, macOS, Linux)|

# C'est bon vous êtes prêt pour fine-tunner ;)