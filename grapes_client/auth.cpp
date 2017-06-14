
#include "stdafx.h"
#include "jsoncpp-src-0.5.0\include\json\json.h"
#include <string>
#include <list>
using namespace std;
#include "swfapi.h"
#include "packet.h"
#include "auth.h"
#include "robot.h"
#include "auth.h"

DWORD WINAPI receive(LPVOID lpParameter)
{
	char buff[20000] = "";
	int length = 0;
	ChatAuth *ca = (ChatAuth *)lpParameter;
	while (true)
	{
		int result = recv(ca->getDouyuSocket(), buff + length, sizeof(buff)-length, 0);
		if (result > 0)
		{
			length += result;
		}
		else
		{
			ca->close();
			break;
		}
		while (true)
		{
			//printf(buff + 12);
			Packet packet = Packet(buff);
			int packet_len = packet.size();
			if (packet_len > 0)
			{
				ca->receivePacket(packet);
				memcpy(buff, buff + packet_len, length - packet_len);
				memset(buff + (length - packet_len), 0, packet_len);
				length -= packet_len;
			}
			else
			{
				break;
			}
		}
	}
	return 0;
}

DWORD WINAPI keeplive_douyu(LPVOID lpParameter)
{
	SOCKET *douyuSocket = (SOCKET *)lpParameter;
	Json::Value swf_req;
	while (true)
	{
		swf_req["func"] = "xxKeepLive";
		swf_req["vbw"] = "0";
		Json::Value swf_rst = Swfapi::xxSwfApi(swf_req);
		Packet packet = Packet(swf_rst["text"].asString());
		if (send(*douyuSocket, packet.to_raw(), packet.size(), 0) > 0)
		{
#ifdef _DEBUG
			cout << "keeplive_douyu" << endl;
#endif // _DEBUG
			Sleep(KEEP_ALIVE_INTERVAL_SECONDS * 1000);
		}
		else
		{
#ifdef _DEBUG
			cout << "keeplive_douyu error:" << WSAGetLastError() << endl;
#endif // _DEBUG
			return -1;
		}
	}
	return 0;
}

ChatAuth::ChatAuth(Robot *const robot, int rid, char * host, int port, Json::Value cookie)
{
	m_robot = robot;
	m_rid = rid;
	strcpy(m_host, host);
	m_port = port;
	m_cookie = cookie;
}

ChatAuth::~ChatAuth()
{
}

SOCKET ChatAuth::getDouyuSocket()
{
	return m_douyuSocket;
}

int ChatAuth::login()
{
	SOCKADDR_IN addrSrv;
	addrSrv.sin_family = AF_INET;
	addrSrv.sin_port = htons(m_port);
	addrSrv.sin_addr.s_addr = inet_addr(m_host);
	m_douyuSocket = socket(AF_INET, SOCK_STREAM, 0);
	if (SOCKET_ERROR == m_douyuSocket) {
#ifdef _DEBUG
		cout << "Socket() error:" << WSAGetLastError() << endl;
#endif // _DEBUG
		return -1;
	}
	int result = connect(m_douyuSocket, (struct  sockaddr*)&addrSrv, sizeof(addrSrv));
	if (INVALID_SOCKET == result)
	{
#ifdef _DEBUG
		cout << "Connect failed:" << WSAGetLastError() << endl;
#endif // _DEBUG
		return -1;
	}
	CreateThread(nullptr, 0, receive, this, 0, nullptr);

	Json::Value swf_req;
	swf_req["func"] = "xxUserLogin";
	swf_req["username"] = m_cookie["acf_username"];
	swf_req["password"] = m_cookie["acf_auth"];
	swf_req["devid"] = m_cookie["acf_devid"];
	swf_req["ltkid"] = m_cookie["acf_ltkid"];
	swf_req["biz"] = m_cookie["acf_biz"];
	swf_req["stk"] = m_cookie["acf_stk"];
	swf_req["roomid"] = to_string(m_rid);
	swf_req["ct"] = m_cookie["acf_ct"];
	swf_req["ver"] = "20150929";
	swf_req["aver"] = "2017052721";
#ifdef _DEBUG
	cout << "xxUserLogin: " << swf_req.toStyledString() << endl;
#endif // _DEBUG
	Json::Value swf_rst = Swfapi::xxSwfApi(swf_req);
	if (swf_rst["text"].empty())
	{
		return -1;
	}
	else
	{
		sendText(swf_rst["text"].asString());
		return 0;
	}
}

int ChatAuth::sendBarrage(string barrage)
{
	Json::Value send_par;
	send_par["type"] = "chatmessage";
	send_par["receiver"] = "0";
	send_par["content"] = barrage;
	return sendJson(send_par);
}

int ChatAuth::close()
{
	closesocket(m_douyuSocket);
	return 0;
}

int ChatAuth::receivePacket(Packet packet)
{
	static int debug_count = 0;
#ifdef _DEBUG
	WCHAR wszBuffer[20000] = L"";
	UINT nLen = MultiByteToWideChar(CP_UTF8, NULL, packet.getString().c_str(), -1, wszBuffer, 20000);
	CHAR szBuff[20000] = "";
	nLen = WideCharToMultiByte(936, NULL, wszBuffer, -1, szBuff, 20000, NULL, NULL);
	cout << "receivePacket: " << szBuff << endl;
	//cout << "receivePacket: " << packet.getJson().toStyledString() << endl;
#endif
	Json::Value swf_req;
	string msg_type = packet.attr("type");
	if (msg_type == "loginres")
	{
		//CreateThread(nullptr, 0, keeplive_douyu, &m_douyuSocket, 0, nullptr);
	}
	else if (msg_type == "cdcp")
	{
		Json::Value json;
		json["type"] = "qtlnq";
		sendJson(json);
	}
	else if (msg_type == "wiru")
	{
		Json::Value json;
		json["type"] = "qtlq";
		sendJson(json);
		CreateThread(nullptr, 0, keeplive_douyu, &m_douyuSocket, 0, nullptr);
		json["type"] = "get_online_noble_list";
		json["rid"] = to_string(m_rid);
		sendJson(json);
		json["type"] = "qrl";
		json["et"] = "0";
		sendJson(json);
	}
	else if (msg_type == "suq")
	{
		swf_req["func"] = "xxSuq";//sus
		swf_req["pwd"] = m_cookie["acf_stk"];
		swf_req["str"] = packet.getString();
		Json::Value swf_rst = Swfapi::xxSwfApi(swf_req);
		sendText(swf_rst["text"].asString());
	}
	else if (msg_type == "vq")
	{
		swf_req["func"] = "xxVq";//vs
		swf_req["str"] = packet.getString();
		Json::Value swf_rst = Swfapi::xxSwfApi(swf_req);
		sendText(swf_rst["text"].asString());
	}
	else if (msg_type == "rlcn")
	{
		debug_count++;
	}
	
	m_robot->callback(packet.getJson());
	return 0;
}

int ChatAuth::sendText(string text)
{
#ifdef _DEBUG
	WCHAR wszBuffer[20000] = L"";
	UINT nLen = MultiByteToWideChar(CP_UTF8, NULL, text.c_str(), -1, wszBuffer, 20000);
	CHAR szBuff[20000] = "";
	nLen = WideCharToMultiByte(936, NULL, wszBuffer, -1, szBuff, 20000, NULL, NULL);
	cout << "sendText: " << szBuff << endl;
	//cout << "sendText: " << text << endl;
#endif
	Packet packet = Packet(text);
	if (send(m_douyuSocket, packet.to_raw(), packet.size(), 0) > 0)
	{
		return 0;
	}
	else
	{
#ifdef _DEBUG
		cout << "sendText error:" << WSAGetLastError() << endl;
#endif // _DEBUG
		return -1;
	}
}

int ChatAuth::sendJson(Json::Value json)
{
	return sendText(serialize(json));
}
