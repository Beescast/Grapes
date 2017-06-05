#-*- coding: utf-8 -*-
 
import time

dbg_flags = {
	'INFO':1,
	'ERR':1,
	'WARN':1,
	'NOTI':1,
	'ALERT':1,
	'DEBUG':1,
	'VERB':1,
}

def dbg_flag_vaild(flag):
	return dbg_flags.get(flag, 0)

def dbg_dump(level, flag, str):
	try :
		if dbg_flags.get(flag) and dbg_flags.get(level):
			tstr = time.strftime('%y/%m/%d %H:%M:%S', time.localtime())
			dstr = "%s %s.%s: %s" % (tstr, level, flag, str)
			print dstr
	except Exception, e:
		print e, level, flag

def dbg_flag_add(flag, default=0):
	dbg_flags[flag] = default

def dbg_info(flag, str):
	dbg_dump("INFO", flag, str)

def dbg_err(flag, str):
	dbg_dump("ERR", flag, str)

def dbg_warn(flag, str):
	dbg_dump("WARN", flag, str)

def dbg_noti(flag, str):
	dbg_dump("NOTI", flag, str)

def dbg_alert(flag, str):
	dbg_dump("ALERT", flag, str)

def dbg_debug(flag, str):
	dbg_dump("DEBUG", flag, str)

def dbg_verb(flag, str):
	dbg_dump("VERB", flag, str)

def dbg_on(flag):
	dbg_flags[flag] = 1

def dbg_off(flag):
	dbg_flags[flag] = 0

def dbg_flags_dump(self):
	for key in dbg_flags:
		state = "off"
		if dbg_flags[key] == 1:
			state = "on"
		print "%6s: %s" % (key, state)

def dbg_set_status(flag, status):
	if status == "on":
		dbg_on(flag)
		return 0
	elif status == "off":
		dbg_off(flag)
		return 0
	else:
		return -1

#End of file
