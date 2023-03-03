# This is how to use the scripts:

- Change the batch/iterate/auto.conf
	- you need to add the external ip of the current host before 127.0.0.1 in the `bind` config, otherwise, another host can not access the kvrocks instance on this server
	- config the migrate.sh, change the config `new_server_host`
