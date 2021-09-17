import sys
import os
sys.path.append(os.path.abspath(os.getcwd()))

from app import test_client
from api.model.optimalPolicy import OptimalPolicy
from api.model.graphs import LabeledGraph, TwoDGraph
from requests.auth import _basic_auth_str
import json

def login(test_client):
    return test_client.post("/auth/login", headers={
        "Authorization": _basic_auth_str("test", "test123")
    }, follow_redirects=True)

# Routing tests
def test_getOptimalPolicies(test_client):
    token = login(test_client)
    assert b"token" in token.data

    tokenObj = json.loads(token.data)
    rv = test_client.get("/api/policy/best", headers={
        "X-Access-Tokens": tokenObj["token"]
    },
    query_string={
        "team": "Blue"
    })
    assert b"policies" in rv.data

def test_getLineGraph(test_client):
    token = login(test_client)
    assert b"token" in token.data

    tokenObj = json.loads(token.data)
    rv = test_client.get("/api/policy/line", headers={
        "X-Access-Tokens": tokenObj["token"]
    },
    query_string={
        "team": "Blue",
        "endAction": "bKills",
        "isProbability": True
    })
    assert b"points" in rv.data

def test_getPieChart(test_client):
    token = login(test_client)
    assert b"token" in token.data

    tokenObj = json.loads(token.data)
    rv = test_client.get("/api/policy/pie", headers={
        "X-Access-Tokens": tokenObj["token"]
    },
    query_string={
        "team": "Blue",
        "startState": 0,
        "startAction": "bKills",
        "hasKills": True
    })
    assert b"points" in rv.data

# Model tests
def test_GetOptimalPolicy(test_client):
    optimal = OptimalPolicy("Blue")
    policy = optimal.GetOptimalPolicy(0, "bKills")
    assert policy[0].action == "bKills"

def test_GetLineGraph(test_client):
    optimal = OptimalPolicy("Blue")
    items = optimal.GetLineGraph("rKills")
    assert isinstance(items, TwoDGraph)

def test_GetPieChart(test_client):
    optimal = OptimalPolicy("Blue")
    items = optimal.GetPieChart(0, "bKills")
    assert isinstance(items, LabeledGraph)