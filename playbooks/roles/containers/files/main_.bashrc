# ~/.bashrc: executed by bash(1) for non-login shells.

case $- in
    *i*) ;;
    *) return;;
esac

shopt -s checkwinsize

export HISTFILESIZE=
export HISTSIZE=
export HISTTIMEFORMAT="[%F %T] "
export HISTCONTROL=ignoreboth
shopt -s histappend

red='\[\e[00;31m\]'
blue='\[\e[01;34m\]'
normal='\[\e[00;00m\]'
export PS1="$red\u$normal@$red\h$normal:$blue\w$normal"'\$ '

export LS_OPTIONS='--color=auto'
eval "`dircolors`"
alias ls='ls --color=auto'
alias ll='ls --color=auto -la'
alias journalctl='journalctl -o short-iso'

source /etc/bash_completion
