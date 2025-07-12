###############
# SHELL UTILS #
###############

# Parse git branch for prompt
function parse_git_branch() {
    git branch 2> /dev/null | sed -n -e 's/^\* \(.*\)/[\1]/p'
}

COLOR_DEF=$'%f'
COLOR_USR=$'%F{243}'
COLOR_DIR=$'%F{197}'
COLOR_GIT=$'%F{39}'
setopt PROMPT_SUBST
# Configures the prompt on shell
export PROMPT='${COLOR_USR}%n ${COLOR_DIR}%~ ${COLOR_GIT}$(parse_git_branch)${COLOR_DEF} $ '

# Homebrew
eval "$(/opt/homebrew/bin/brew shellenv)"

##########
# PYTHON #
##########

# Pyenv
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - zsh)"

# Postgres - note the version works for me
PATH="$(brew --prefix postgresql@13)/bin:$PATH"

function help_emily () {
  echo "custom shell functions:"
  
  echo "DOCKER: "
  echo "  - dc (uses COMPOSE_FILEPATH) for ease of operations)"
  echo "  - set_compose_file"
  echo "  - view_compose_file"
  echo "  - run_docker_ecr"

  echo "GIT:"
  echo "  - commit_diff"

  echo "K8s: "
  echo " - kpssh " 
  echo " - kpdebug"
  echo " - kpname"

  echo "NAVIGATION: "
  echo "  - nav <dir> (dir options available with nav --help)"


  echo "UTILS:"
  echo "  - do_source (lazy way to resource zsh)"
  echo "  - string_in (i can never remember grep patterns)"
  echo "  - histsearch (look for commands i used)"
}

#########
# UTILS #
#########

# Look at history of commands in shell history
function histsearch() {
  fc -lim "*$@*" 1 
}

# General - find string in stuff
function string_in() {
  grep -rnwi $1 $2
}

# lazy resource shell
function do_source() {
  source ~/.zshrc
}

# Direnv
eval "$(direnv hook zsh)"


# NVM
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# lazy navigation from shell:

## Dev paths for nav function
export DEV_ROOT="$HOME/Development"
# In work contexts I tend to have more paths....
function nav () {
  case $1 in
    -h|--help)
      echo "Usage: nav [option]"
      echo "Options:"
      echo "  development  Navigate to ${DEV_ROOT:-'(not set)'}"
      echo "  -h, --help   Show this help message"
      ;;
    development)
      cd "$DEV_ROOT" || echo "Error: Directory ${DEV_ROOT} not found"
      ;;
    *)
      echo "Invalid option. Use 'nav --help' for usage information."
      ;;
  esac
}


#######
# K8s #
#######

# get pod name
function kpname() {
  local namespace="${2:-emily-default}"
  kubectl get pods -n "$namespace" -o=jsonpath='{range.items..metadata}{.name}{"\n"}{end}' | fgrep $1
}  

# ssh into pod
function kpssh() {
  local namespace="${2:-emily-default}"
  kubectl exec -it "$1" -n "$namespace" -- /bin/sh
}

# creates a debug k8s pod for me to run 
function kpdebug() {
  local namespace="${2:-emily-default}"
  echo $1
  echo $namespace
  kubectl run emily-debug-pod --rm -it --restart=Never --image="$1" --namespace="$namespace" --serviceaccount=emily-example-sa --command -- /bin/sh
}

#######
# GIT #
#######

# Look at diff
function commit_diff() {
   git show --color --pretty=format:%b $1
}

##########
# DOCKER #
##########

# Useful when there's more than one compose file in a project
# e.g. in monorepo contexts
function set_compose_file() {
    export COMPOSE_FILEPATH="$(pwd)/${1}"
}

# View the compose file that has been set 
function view_compose_file() {
  echo $COMPOSE_FILEPATH
}

# interface for easily using env var compose file
function dc() {
  echo "Running: docker-compose -f \"$(view_compose_file)\" $@"
  docker-compose -f "$(view_compose_file)" "$@"
}

# this is useful when running from a Mac - as I often am
function run_docker_ecr() {
  aws ecr get-login-password | docker login --username $2 --password-stdin $3
  docker pull --platform linux/amd64 $1
  docker run --platform linux/amd64 -it --rm $1
}
