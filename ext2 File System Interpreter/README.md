Run "make" in order to produce an executable called fsdump. 
fsdump can be called as ./fsdump <diskimg> 
The argument provided here is a disk image that must be in ext2 format. 
This program will analyze and interpret the disk image file. 
You can also run make clean to remove the object and executable file. 

There are no limitations! 
It is similar to the dumpe2fs and debugfs command. It will provide information on the superblock,
groups, inodes, directory entries and indirect blocks. It is quite an interesting
engineering feat given that there is barely any documentation out there to help out...
Thank you CS nerds! 