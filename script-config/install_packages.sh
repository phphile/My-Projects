#!/usr/bin/env bash
list=( "git" "wget" "curl" "vim" )




# Configurer les paquets
config(){
name=$(printf ".%src" "$1")
path=$(printf "%s/.%src" "$HOME" "$1")
git_path=$(printf "%s/.gitconfig" "$HOME")
user=$(whoami)
email="le_p@etna-alternance.net"
#echo "$name"
file_exists=$(find $HOME -type f -name "$name")
if [[ "$1" == "git" ]]; then 
	git config --global user.name "$user"
	git config --global user.email "$email"
	git config --global core.editor vim
	git config --global init.defaultBranch main
	chmod +x "$git_path"
	#source "$git_path" 
	echo "git successfully configured (user, email, editor, branch)"
else
	if [[ $file_exists ]]; then
		printf "%s configuration file already there\n" "$1" 
		chmod +x "$path"
		source "$path"
		[[ $? ]] && printf "%s configured\n" "$1" || printf "%s not configured\n"	
	else 
		touch "$path"
		printf "%s configuration file created\n" "$1"
		chmod +x "$path"
		source "$path"
	fi
fi
}

# Main program: verifier si package existe, si oui passer a la configuration, si non installer puis configurer  
for pkg in ${list[@]}
do 
	printf "\n"
	pkg_exists=$(dpkg -L "$pkg"  2>/dev/null)
	if [[ $pkg_exists ]]; then 
		printf "%s already there\n" "$pkg"
		config "$pkg"
	else	
		echo "Installing %s...\n" "$pkg"
		sudo apt install "$pkg" -y 
		[[ $? ]] && printf "\n%s successfully installed\n" "$pkg" || printf "Error %s not installed\n" "$pkg"	
	fi
done

#config 
