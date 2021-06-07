# SOURCE this file in Bash, like:
# 
#   $ source "$(git rev-parse --show-toplevel)/dev/bash/env.inc.bash"
# 

# Avoids errors running `ansible-playbook` that look like:
# 
#   objc[35781]: +[__NSPlaceholderDate initialize] may have been in progress in another thread when fork() was called.
#   objc[35781]: +[__NSPlaceholderDate initialize] may have been in progress in another thread when fork() was called. We cannot safely call it or ignore it in the fork() child process. Crashing instead. Set a breakpoint on objc_initializeAfterForkError to debug.
#   ERROR! A worker was found in a dead state
# 
# Why..? Fuck knows man..
# 
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
