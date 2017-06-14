#include "stdafx.h"
#include "utils.h"

int pack(char *buff, Json::Value json)
{
	int len = (int)json.toStyledString().length()+2;
	*(unsigned short *)buff = (unsigned short)len;
	strcpy(buff + 2, json.toStyledString().c_str());
	return len;
}

int unpack(Json::Value &json, char *buff)
{
	int len = *(unsigned short *)buff;
	char buff_str[1024] = "";
	if (len > 2)
	{
		memcpy(buff_str, buff + 2, len - 2);
		if (strlen(buff_str) == len - 2)
		{
			Json::Reader reader;
			reader.parse(buff_str, json);
			return len;
		}
	}
	return 0;
}

string replace(string srcString, string oldString, string NewString)
{
	for (size_t index = srcString.find(oldString);
		index != string::npos;
		index = srcString.find(oldString, index + oldString.length()))
	{
		srcString.replace(index, oldString.length(), NewString);
	}
	return srcString;
}

string escape(string value)
{
	value = replace(value, "@", "@A");
	value = replace(value, "/", "@S");
	return value;
}

string unescape(string value)
{
	value = replace(value, "@S", "/");
	value = replace(value, "@A", "@");
	return value;
}

string serialize(Json::Value data)
{
	string str = string();
	if (data.empty())
	{
		return string();
	}
	list<string> kv_pairs;
	Json::Value::Members members = data.getMemberNames();
	for (Json::Value::Members::iterator i = members.begin();
		i != members.end(); i++)
	{
		string &name = *i;
		string str = string(data[name].asString());
		kv_pairs.push_back(name + "@=" + data[name].asString());
	}
	for (list<string>::iterator i = kv_pairs.begin(); i != kv_pairs.end(); i++)
	{
		str += *i + "/";
	}
	return str;
}

Json::Value deserialize(string value)
{
	Json::Value result;
	if (value.length() <= 0)
	{
		return result;
	}
	list<string> kv_pairs;
	size_t start = 0;
	for (size_t index = value.find("/");
		index != string::npos;
		index = value.find("/", start))
	{
		kv_pairs.push_back(value.substr(start, index - start));
		start = index + 1;
	}
	if (0 == start)
	{
		return Json::Value(value);
	}
	for (list<string>::iterator i = kv_pairs.begin();
		i != kv_pairs.end(); i++)
	{
		string kv_pair = *i;
		if (kv_pair.length() <= 0)
		{
			continue;
		}
		size_t index = kv_pair.find("@=");
		if (index == string::npos)
		{
			continue;
		}
		string k = unescape(kv_pair.substr(0, index));
		string v = unescape(kv_pair.substr(index + 2, kv_pair.length() - (index + 2)));
		index = v.find("@=");
		if (string::npos != index)
		{
			result[k] = deserialize(v);
		}
		else if (v.find("/") != string::npos)
		{
			Json::Value lv;
			list<string> lkv_pairs;
			start = 0;
			for (size_t index = v.find("/");
				index != string::npos;
				index = v.find("/", start))
			{
				lkv_pairs.push_back(v.substr(start, index - start));
				start = index + 1;
			}
			for (list<string>::iterator i = lkv_pairs.begin();
				i != lkv_pairs.end(); i++)
			{
				string lkv_pair = *i;
				if (lkv_pair.length() <= 0)
				{
					continue;
				}
				lv.append(deserialize(unescape(lkv_pair)));
			}
			result[k] = lv;
		}
		else
		{
			result[k] = v;
		}
	}
	return result;
}
