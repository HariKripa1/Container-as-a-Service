import nodejsbuild
user = input('user');
print(user);
giturl = input('giturl');
print(giturl);
srcpath = input('srcpath');
print(srcpath);
nodejsbuild.nodeJsBuild(user,giturl,srcpath)
print('call end');