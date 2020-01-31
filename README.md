# Amigoshan.github.io
amigo website

This is wenshan's personal website.

This website simply employ html, css with jekyll framework. 

Some advantage features:
 -- comments with duoshuo
 -- website statistics with youmeng

Download and setup: 
* Setup the environment
```sudo apt-get install ruby-full build-essential zlib1g-dev```
```
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```
```gem install jekyll bundler```
* Clone the project and build
```bundle init```
```bundle exec jekyll serve```