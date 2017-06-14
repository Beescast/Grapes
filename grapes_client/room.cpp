
#include "stdafx.h"
#include "jsoncpp-src-0.5.0\include\json\json.h"
#include <WinSock2.h>
#include <list>
using namespace std;
#include "packet.h"
#include "auth.h"
#include "robot.h"
#include "room.h"

DWORD WINAPI room_run(LPVOID lpParameter)
{
	Room *room = (Room *)lpParameter;
	room->run();
	return 0;
}

Room::Room(int rid)
{
	m_rid = rid;

	//CreateThread(nullptr, 0, room_run, this, 0, nullptr);
}

Room::~Room()
{
	list<Robot*>::iterator i = m_robots.begin();
	while (i != m_robots.end())
	{
		Robot *robot = *i;
		robot->close();
		m_robots.remove(robot);
		i = m_robots.begin();
	}
}

int Room::getRoomId()
{
	return m_rid;
}

bool Room::isEmpty()
{
	if (m_robots.size() > 0)
	{
		return false;
	}
	else
	{
		return true;
	}
}

int Room::run()
{
	return 0;
}

int Room::close()
{
	list<Robot*>::iterator i = m_robots.begin();
	while (i != m_robots.end())
	{
		Robot *robot = *i;
		robot->close();
		m_robots.remove(robot);
		i = m_robots.begin();
	}
	return 0;
}

int Room::addCookie(Json::Value cookie, bool status, int freq)
{
	Robot *robot = new Robot(m_rid, cookie, status, freq);
	robot->setSocketServer(m_socketServer);
	m_robots.push_back(robot);
	return 0;
}

int Room::delCookie(int uid)
{
	Robot *robot = getRobot(uid);
	if (robot != nullptr)
	{
		robot->close();
	}
	return 0;
}

int Room::setSpeak(bool status)
{
	for (list<Robot*>::iterator i = m_robots.begin(); i != m_robots.end(); i++)
	{
		Robot *robot = *i;
		robot->setSpeak(status);
	}
	return 0;
}

int Room::setFreq(int freq)
{
	for (list<Robot*>::iterator i = m_robots.begin(); i != m_robots.end(); i++)
	{
		Robot *robot = *i;
		robot->setFreq(freq);
	}
	return 0;
}

int Room::sendBarrage(int uid, string barrage)
{
	Robot *robot = getRobot(uid);
	if (robot != nullptr)
	{
		robot->sendBarrage(barrage);
	}
	return 0;
}

void Room::setSocketServer(SOCKET socketServer)
{
	m_socketServer = socketServer;
}

Robot * Room::getRobot(int uid)
{
	for (list<Robot*>::iterator i = m_robots.begin(); i != m_robots.end(); i++)
	{
		Robot *robot = *i;
		if (uid == robot->getUid())
		{
			return robot;
		}
	}
	return nullptr;
}
