
#include "stdafx.h"
#include "jsoncpp-src-0.5.0\include\json\json.h"
#include <string>
#include <time.h>
#include <WinSock2.h>
using namespace std;
#include "config.h"
#include "servers.h"
#include "packet.h"
#include "auth.h"
#include "robot.h"

DWORD WINAPI robot_run(LPVOID lpParameter)
{
	Robot *robot = (Robot *)lpParameter;
	robot->loopBarrage();
	return 0;
}

int Robot::callback(Json::Value value)
{
	if (value["type"].asString() == "error")
	{
		int code = atoi(value["code"].asCString());
		if (51 == code)
		{
			return 0;
		}
		else
		{
			char buff[1024] = "";
			Json::Value value;
			value["code"] = code;
			value["type"] = CMD_CLIENT_DOUYU_ERROR;
			Json::Value params;
			params["rid"] = m_rid;
			params["uid"] = m_uid;
			value["data"] = params;
			value["timestamp"] = (unsigned int)time(nullptr);
#ifdef _DEBUG
			cout << "douyu_error: " << value.toStyledString() << endl;
#endif // _DEBUG
			int len = pack(buff, value);
			if (send(m_socketServer, buff, len, 0) > 0)
			{
				return 0;
			}
			else
			{
#ifdef _DEBUG
				cout << "douyu_error error:" << WSAGetLastError() << endl;
#endif // _DEBUG
				return -1;
			}
		}
	}
	return 0;
}

Robot::Robot(int rid, Json::Value cookie, bool status, int freq)
{
	m_rid = rid;
	m_uid = atoi(cookie["acf_uid"].asCString());
	m_speak = status;
#ifdef _DEBUG
	if (freq < 6)
	{
		freq = 6;
	}
#else
	if (freq < 20)
	{
		freq = 20;
	}
#endif // _DEBUG
	m_freq = freq;//此为随机发言间隔最大值
	m_sendCount = 0;
#ifdef _DEBUG
	m_sendMax = rand() % 2 + 2;//[2, 4)
#else
	m_sendMax = rand() % 20 + 20;//[20, 40)
#endif // _DEBUG
	m_isRunning = true;

	struct DouYuServer ds = douyuServers[rand() % DERVER_NUM];
#ifdef _DEBUG
	cout << "use server: [" << ds.ip << ":" << ds.port << "]" << endl;
#endif // _DEBUG
	m_auth = new ChatAuth(this, m_rid, ds.ip, ds.port, cookie);
	m_auth->login();
	CreateThread(nullptr, 0, robot_run, this, 0, nullptr);
}

Robot::~Robot()
{
	m_auth->close();
	m_auth = nullptr;
}

int Robot::setSpeak(bool status)
{
	m_speak = status;
	return 0;
}

int Robot::setFreq(int freq)
{
#ifdef _DEBUG
	if (freq < 6)
	{
		freq = 6;
	}
#else
	if (freq < 20)
	{
		freq = 20;
	}
#endif // _DEBUG
	m_freq = freq;
	return 0;
}

int Robot::sendBarrage(string barrage)
{
	m_auth->sendBarrage(barrage);
	if (m_sendCount > m_sendMax)
	{
		char buff[1024] = "";
		Json::Value value;
		value["code"] = 0;
		value["type"] = CMD_CLIENT_COOKIE;
		Json::Value params;
		params["rid"] = m_rid;
		params["uid"] = m_uid;
		value["data"] = params;
		value["timestamp"] = (unsigned int)time(nullptr);
#ifdef _DEBUG
		cout << "sendBarrage: " << value.toStyledString() << endl;
#endif // _DEBUG
		close();
		int len = pack(buff, value);
		if (send(m_socketServer, buff, len, 0) > 0)
		{
			return 0;
		}
		else
		{
#ifdef _DEBUG
			cout << "sendBarrage error:" << WSAGetLastError() << endl;
#endif // _DEBUG
			return -1;
		}
	}
	m_sendCount++;
	return 0;
}

void Robot::setSocketServer(SOCKET socketServer)
{
	m_socketServer = socketServer;
}

int Robot::getUid()
{
	return m_uid;
}
/*
int Robot::run()
{
	//CreateThread(nullptr, 0, robot_run, this, 0, nullptr);
	return 0;
}
*/
int Robot::loopBarrage()
{
	while (m_isRunning)
	{
		int freq = rand() % (m_freq - 19) + 20;//[20, m_freq)
		Sleep(freq * 1000);
		if (m_speak)
		{
			char buff[1024] = "";
			Json::Value value;
			value["code"] = 0;
			value["type"] = CMD_CLIENT_BARRAGE;
			Json::Value params;
			params["rid"] = m_rid;
			params["uid"] = m_uid;
			value["data"] = params;
			value["timestamp"] = (unsigned int)time(nullptr);
#ifdef _DEBUG
			cout << "loopBarrage: " << value.toStyledString() << endl;
#endif // _DEBUG
			int len = pack(buff, value);
			if (send(m_socketServer, buff, len, 0) <= 0)
			{
#ifdef _DEBUG
				cout << "loopBarrage error:" << WSAGetLastError() << endl;
#endif // _DEBUG
				close();
				return -1;
			}
		}
	}
	return 0;
}

int Robot::close()
{
	m_isRunning = false;
	m_auth->close();
	return 0;
}
