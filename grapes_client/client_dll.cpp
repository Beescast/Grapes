// client_dll.cpp : 定义 DLL 应用程序的导出函数。
//

#include "stdafx.h"
#include "jsoncpp-src-0.5.0\include\json\json.h"
#include <WinSock2.h>
#include <WS2tcpip.h>
#include <time.h>
#include <iostream>
using namespace std;
#include "utils.h"
#include "config.h"
#include "packet.h"
#include "auth.h"
#include "robot.h"
#include "room.h"
#include "manage.h"
#include "client_dll.h"

#pragma comment(lib, "ws2_32.lib")

DWORD WINAPI keeplive(LPVOID lpParameter)
{
	char buff[1024] = "";
	SOCKET socketServer = *(SOCKET *)lpParameter;

	while (true)
	{
		Json::Value value;
		value["code"] = CODE_SUCCESS;
		value["type"] = CMD_CLIENT_KEEPLIVE;
		value["data"] = Json::nullValue;
		value["timestamp"] = (unsigned int)time(nullptr);
#ifdef _DEBUG
		//cout << "keeplive: " << value.toStyledString() << endl;
#endif // _DEBUG
		int len = pack(buff, value);
		if (send(socketServer, buff, len, 0) > 0)
		{
			Sleep(KEEPLIVE_INTERVAL);
		}
		else
		{
#ifdef _DEBUG
			cout << "keeplive error:" << WSAGetLastError() << endl;
#endif // _DEBUG
			break;
		}
	}
	return 0;
}

int freq_hdlr(Manage *manage, Json::Value json)
{
#ifdef _DEBUG
	cout << "freq_hdlr: " << json.toStyledString() << endl;
#endif
	int code = json["code"].asInt();
	if (CODE_SUCCESS == code)
	{
		Json::Value data = json["data"];
		int rid = data["rid"].asInt();
		int freq = data["freq"].asInt();
		manage->setFreq(rid, freq);
		return 0;
	}
	return -1;
}

int speak_hdlr(Manage *manage, Json::Value json)
{
#ifdef _DEBUG
	cout << "speak_hdlr: " << json.toStyledString() << endl;
#endif
	int code = json["code"].asInt();
	if (CODE_SUCCESS == code)
	{
		Json::Value data = json["data"];
		int rid = data["rid"].asInt();
		bool speak = data["speak"].asBool();
		manage->setSpeak(rid, speak);
		return 0;
	}
	return -1;
}

int addCookie_hdlr(Manage *manage, Json::Value json)
{
#ifdef _DEBUG
	cout << "addCookie_hdlr: " << json.toStyledString() << endl;
#endif
	int code = json["code"].asInt();
	if (CODE_SUCCESS == code)
	{
		Json::Value data = json["data"];
		int rid = data["rid"].asInt();
		Json::Value cookie = data["cookie"];
		bool status = data["speak"].asBool();
		int freq = data["freq"].asInt();
		manage->addCookie(rid, cookie, status, freq);
		return 0;
	}
	return -1;
}

int delCookie_hdlr(Manage *manage, Json::Value json)
{
#ifdef _DEBUG
	cout << "delCookie_hdlr: " << json.toStyledString() << endl;
#endif
	int code = json["code"].asInt();
	if (CODE_SUCCESS == code)
	{
		Json::Value data = json["data"];
		int rid = data["rid"].asInt();
		int uid = data["uid"].asInt();
		manage->delCookie(rid, uid);
		return 0;
	}
	return -1;
}

int barrage_hdlr(Manage *manage, Json::Value json)
{
#ifdef _DEBUG
	cout << "barrage_hdlr: " << json.toStyledString() << endl;
#endif
	int code = json["code"].asInt();
	if (CODE_SUCCESS == code)
	{
		Json::Value data = json["data"];
		int rid = data["rid"].asInt();
		int uid = data["uid"].asInt();
		string barrage = data["barrage"].asString();
		manage->sendBarrage(rid, uid, barrage);
		return 0;
	}
	return -1;
}

int delRoom_hdlr(Manage *manage, Json::Value json)
{
#ifdef _DEBUG
	cout << "delRoom_hdlr: " << json.toStyledString() << endl;
#endif
	int code = json["code"].asInt();
	if (CODE_SUCCESS == code)
	{
		Json::Value data = json["data"];
		int rid = data["rid"].asInt();
		manage->delRoom(rid);
		return 0;
	}
	return 0;
}

int keeplive_hdlr(Manage *manage, Json::Value json)
{
#ifdef _DEBUG
	cout << "keeplive_hdlr: " << json.toStyledString() << endl;
#endif
	return 0;
}

typedef int(*CmdCallback)(Manage *, Json::Value);

struct CmdStruct {
	int code;
	CmdCallback callback;
};

//extern "C" __declspec(dllexport) int __stdcall GrapesClient()
int GrapesClient()
{
	struct CmdStruct CmdArr[] = {
		{ CMD_SERVER_FREQ, freq_hdlr },
		{ CMD_SERVER_SPEAK, speak_hdlr },
		{ CMD_SERVER_ADDCOOKIE, addCookie_hdlr },
		{ CMD_SERVER_DELCOOKIE, delCookie_hdlr },
		{ CMD_SERVER_BARRAGE, barrage_hdlr },
		{ CMD_SERVER_DELROOM, delRoom_hdlr },
		{ CMD_SERVER_KEEPLIVE, keeplive_hdlr },
	};
	SOCKET socketServer;
	//cout << "Hello world!" <<endl;
	WSADATA wsaData;
	char buff[MAX_RECV_SIZE] = { 0 };
	int length = 0;
	srand(time(nullptr));

	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
	{
#ifdef _DEBUG
		cout << "Failed to load Winsock" << endl;
#endif // _DEBUG
		return -1;
	}

#ifdef _DEBUG
	Json::Value cookie;
	cookie["acf_username"] = "";
	cookie["acf_auth"] = "";
	cookie["acf_devid"] = "A4E141DEB649FACA18356000843008F1";
	cookie["acf_ltkid"] = "";
	cookie["acf_biz"] = "";
	cookie["acf_stk"] = "";
	cookie["acf_ct"] = "0";
	//manage.addCookie(1876728, cookie, false, 30);
#endif

	SOCKADDR_IN addrSrv;
	addrSrv.sin_family = AF_INET;
	addrSrv.sin_port = htons(SERVER_PORT);
	addrSrv.sin_addr.s_addr = inet_addr(SERVER_IP);
	while (true)
	{
		Manage manage = Manage();
		socketServer = socket(AF_INET, SOCK_STREAM, 0);
		if (SOCKET_ERROR == socketServer)
		{
#ifdef _DEBUG
			cout << "Socket() error:" << WSAGetLastError() << endl;
			Sleep(6 * 1000);
#else
			Sleep(60 * 1000);
#endif // _DEBUG
			return -1;
		}
		manage.setSocketServer(socketServer);

		int result = connect(socketServer, (struct sockaddr*)&addrSrv, sizeof(addrSrv));
		if (INVALID_SOCKET == result)
		{
#ifdef _DEBUG
			cout << "Connect failed:" << WSAGetLastError() << endl;
			Sleep(6 * 1000);
#else
			Sleep(60 * 1000);
#endif // _DEBUG
			continue;
		}
		CreateThread(nullptr, 0, keeplive, &socketServer, 0, nullptr);
		while (true)
		{
			result = recv(socketServer, buff+length, MAX_RECV_SIZE, 0);
			if (result > 0)
			{
				length += result;
				while (true)
				{
					Json::Value json;
					int len = unpack(json, buff);
					if (len > 2)
					{
#ifdef _DEBUG
						//cout << json.toStyledString() << endl;
#endif // _DEBUG
						for (int i = 0; i < sizeof(CmdArr) / sizeof(CmdArr[0]); i++)
						{
							if (json["type"] == CmdArr[i].code)
							{
								CmdArr[i].callback(&manage, json);
							}
						}
						length -= len;
						memcpy(buff, buff + len, length);
						memset(buff + length, 0, sizeof(buff) / sizeof(buff[0]) - length);
					}
					else
					{
						break;
					}
				}
			}
			else
			{
				manage.close();
#ifdef _DEBUG
				cout << "recv failed:" << WSAGetLastError() << endl;
				Sleep(6 * 1000);
#else
				Sleep(60 * 1000);
#endif // _DEBUG
				break;
			}
		}
	}

	closesocket(socketServer);
	WSACleanup();
	return 0;
}
