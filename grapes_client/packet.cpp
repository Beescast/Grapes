
#include "stdafx.h"
#include "packet.h"


Packet::Packet(string body)
{
	memset(m_pack.buff, 0, sizeof(m_pack.buff));
	m_pack.protocol.msg_len = body.length() + 8 + 1;
	m_pack.protocol.msg_len_bak = m_pack.protocol.msg_len;
	m_pack.protocol.msg_type = MESSAGE_TYPE_FROM_CLIENT;
	m_pack.protocol.reserved = 0;
	strcpy(m_pack.protocol.data, body.c_str());
	m_json = deserialize(body);
}

Packet::Packet(char * buff)
{
	memset(m_pack.buff, 0, sizeof(m_pack.buff));
	memcpy(m_pack.buff, buff, 12);
	if ((m_pack.protocol.msg_len == m_pack.protocol.msg_len_bak)
		&& ((MESSAGE_TYPE_FROM_CLIENT == m_pack.protocol.msg_type)
			|| (MESSAGE_TYPE_FROM_SERVER == m_pack.protocol.msg_type)))
	{
		memcpy(m_pack.protocol.data, buff + 12, m_pack.protocol.msg_len-8);
		if (strlen(m_pack.protocol.data) != m_pack.protocol.msg_len - 8-1)
		{
			memset(m_pack.buff, 0, sizeof(m_pack.buff));
		}
		else
		{
			m_json = deserialize(m_pack.protocol.data);
		}
	}
	else
	{
		memset(m_pack.buff, 0, 12);
	}
}

Packet::~Packet()
{

}

char * Packet::to_raw()
{
	return m_pack.buff;
}

int Packet::size()
{
	if (0 == m_pack.protocol.msg_len)
	{
		return 0;
	}
	return strlen(m_pack.protocol.data) + 12 + 1;
}

Json::Value Packet::getJson()
{
	return m_json;
}

string Packet::getString()
{
	return string(m_pack.protocol.data);
}

string Packet::attr(string attrName)
{
	return m_json[attrName].asString();
}