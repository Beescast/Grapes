
#include "stdafx.h"
#include "jsoncpp-src-0.5.0\include\json\json.h"
#include <WinSock2.h>
#include <list>
#include <string>
#include <iostream>
using namespace std;
#include "packet.h"
#include "auth.h"
#include "robot.h"
#include "room.h"
#include "manage.h"

Manage::Manage()
{
	
}

Manage::~Manage()
{
	list<Room*>::iterator i = m_rooms.begin();
	while (i != m_rooms.end())
	{
		Room *room = *i;
		room->close();
		m_rooms.remove(room);
		i = m_rooms.begin();
	}
}

int Manage::addRoom(int rid)
{
	if (!inRooms(rid))
	{
		Room *room = new Room(rid);
		room->setSocketServer(m_socketServer);
		m_rooms.push_back(room);
#ifdef _DEBUG
		cout << "add room:" << rid << endl;
#endif // _DEBUG
		return 0;
	}
	return 0;//房间已在列表中
}

int Manage::delRoom(int rid)
{
	Room *room = getRoom(rid);
	if (nullptr != room)
	{
		if (room->isEmpty())
		{
			m_rooms.remove(room);
#ifdef _DEBUG
			cout << "del room:" << rid << endl;
#endif // _DEBUG
			return 0;//删除成功
		}
		else
		{
			return 0;//房间里还有账号，并未删除
		}
	}
	return 0;//列表里面并没有这个房间
}

int Manage::addCookie(int rid, Json::Value cookie, bool status, int freq)
{
	addRoom(rid);
	Room *room = getRoom(rid);
	if (room != nullptr)
	{
		room->addCookie(cookie, status, freq);
#ifdef _DEBUG
		cout << "set room:" << rid << " addCookie:" << cookie << endl;
#endif // _DEBUG
	}
	return 0;
}

int Manage::delCookie(int rid, int uid)
{
	Room *room = getRoom(rid);
	if (room != nullptr)
	{
		room->delCookie(uid);
#ifdef _DEBUG
		cout << "set room:" << rid << " delCookie:" << uid << endl;
#endif // _DEBUG
		delRoom(rid);
	}
	return 0;
}

int Manage::setSpeak(int rid, bool status)
{
	Room *room = getRoom(rid);
	if (room != nullptr)
	{
		room->setSpeak(status);
#ifdef _DEBUG
		cout << "set room:" << rid << " speak:" << status << endl;
#endif // _DEBUG
	}
	return 0;
}

int Manage::setFreq(int rid, int freq)
{
	Room *room = getRoom(rid);
	if (room != nullptr)
	{
		room->setFreq(freq);
#ifdef _DEBUG
		cout << "set room:" << rid << " freq:" << freq << endl;
#endif // _DEBUG
	}
	return 0;
}

int Manage::sendBarrage(int rid, int uid, string barrage)
{
	Room *room = getRoom(rid);
	if (room != nullptr)
	{
		room->sendBarrage(uid, barrage);
#ifdef _DEBUG
		cout << "set room:" << rid << " uid:" << uid << " barrage:" << barrage << endl;
#endif // _DEBUG
	}
	return 0;
}

void Manage::setSocketServer(SOCKET socketServer)
{
	m_socketServer = socketServer;
}

SOCKET Manage::getSocketServer()
{
	return m_socketServer;
}

int Manage::close()
{
	list<Room*>::iterator i = m_rooms.begin();
	while (i != m_rooms.end())
	{
		Room *room = *i;
		room->close();
		m_rooms.remove(room);
		i = m_rooms.begin();
	}
	return 0;
}

Room * Manage::getRoom(int rid)
{
	for (list<Room*>::iterator i = m_rooms.begin(); i != m_rooms.end(); i++)
	{
		Room *room = *i;
		if (room->getRoomId() == rid)
		{
			return room;
		}
	}
	return nullptr;
}

bool Manage::inRooms(int rid)
{
	bool in_flag = false;
	for (list<Room*>::iterator i = m_rooms.begin(); i != m_rooms.end(); i++)
	{
		Room *room = *i;
		if (rid == room->getRoomId())
		{
			in_flag = true;
			break;
		}
	}
	return in_flag;
}
