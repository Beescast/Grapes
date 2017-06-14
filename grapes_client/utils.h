#pragma once
#include "jsoncpp-src-0.5.0\include\json\json.h"
#include <iostream>
#include <list>
using namespace std;

int pack(char *buff, Json::Value json);
int unpack(Json::Value &json, char *buff);
string escape(string value);
string unescape(string value);
string serialize(Json::Value data);
Json::Value deserialize(string value);