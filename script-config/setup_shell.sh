#!/usr/bin/env bash
plugins=("git" "zsh-completions")


#DEPLOY OH MY ZSH

run_ohmyzsh(){
path=$(printf "%s/.oh-my-zsh/oh-my-zsh.sh" "$HOME")
source "$path"
}



#INSTALL OH MY ZSH

install_ohmyzsh(){
ohmyzsh_exists=$(find $HOME -type d -name ".oh-my-zsh")
if [[ $ohmyzsh_exists ]]; then 
	echo "oh-my-zsh already there"
else 
	echo "Installing Oh my zsh..."	
	sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
	if [[ $? ]]; then 
		echo "oh-my-zsh successfully installed"
		
	else
		echo "error oh-my-zsh not installed"
	fi
fi
}



#CONFIGURER ZSH AVEC PLUGINS, AUTOCOMPLETION DES COMMANDES, THEME ET ALIAS 

config_zsh(){
path=$(printf "%s/.zshrc" "$HOME") 
printf "\nAdding auto completetion ...\n"
compinit_exists=$(cat "$path" | grep "compinit")
if [[ $compinit_exists ]]; then 
	echo "compinit already added"
else 
	echo "autoload -Uz compinit; compinit" >> "$path"
	[[ $? ]] && echo "compinit added successfully" || echo "Error: compinit not added"
fi

for plugin in ${plugins[@]}
do
	pattern=$(printf "^plugins=(%s)" "$plugin")	
	check_plugin=$(cat "$path" | grep "$pattern")
	if ! [[ $check_plugin ]]; then 
		printf "\nplugins=(%s)" "$plugin" >> "$path"
		[[ $? ]] && printf "%s plugin added\n" "$plugin" || printf "cannot add %s plugin\n" "$plugin"
	else
		printf "Plugin %s already there\n" "$plugin"
	fi
	done


printf "\nAdding aliases ...\n"
alias="alias gcl='git clone' gcm='git commit -m' gp='git push'" 
alias_exists=$(cat "$path" | grep "^$alias")
if [[ $alias_exists ]]; then 
	echo "Aliases already added"
else 
	printf "\n%s" "$alias" >> "$path"
	[[ $? ]] && echo "Aliases successfully added"  || echo "Error aliases not added"
fi


printf "\nSetting theme...\n"
theme_exists=$(cat "$path" | grep "ZSH_THEME")
if [[ $theme_exists ]]; then 
	sed -i '/^ZSH_THEME/d' "$path"
	printf '\nZSH_THEME="af-magic"' >> "$path"
	[[ $? ]] && echo "Theme succesfully added" || echo "Error them not added"
else 
	printf '\nZSH_THEME="af-magic"' >> "$path"
        [[ $? ]] && echo "Theme succesfully added" || echo "Error them not added"
fi
}



# MAKE ZSH DEFAULT SHELL

set_default(){
user=$(whoami)
sudo usermod -s /bin/zsh "$user" >/dev/null
if [[ $? ]]; then 
	echo "Zsh is now default shell"
	#run_ohmyzsh
else
	 echo "error zsh not default shell"
fi
}


#ACTIVER LES CONFIGURATIONS DE ZSH

run_zsh(){
path=$(printf "%s/.zshrc" "$HOME")
zsh=$(command -v zsh)
install_ohmyzsh
echo "Configuring zsh..."
config_zsh
#source "$path"
if [[ $? ]]; then
	echo "zsh configured successfully"
	set_default
	eval $(printf " %s %s" "$zsh" "$path") 2>/dev/null
	exec zsh
else 
	 echo "zsh not configured"
fi
}


#MAIN PROGRAM 

zsh_exists=$(dpkg -L zsh 2>/dev/null)
printf "\n"
if [[ $zsh_exists ]]; then
	echo "zsh already there"
	run_zsh
else 
	sudo apt install zsh -y
	if [[ $? ]]; then 
		echo "zsh successfully installed"
		run_zsh
	else	
		echo "Error zsh not installed"
	fi
fi 
