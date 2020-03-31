# use 'source snippets/clear_buff_cache.sh' to execute
free && sync && echo 3 > /proc/sys/vm/drop_caches && free