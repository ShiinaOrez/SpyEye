package main

import "sync"

type Position struct {
	X        int64
	Y        int64
}

type Report struct {
	Time     float64
	IsBtn    bool
	Pos      Position
	Width    int64
}

type Track struct {
	ID       int64
	Reports  []Report
}

type Slot struct {
	Tracks   []Track
	Used     bool
}

type Collection struct {
	Slots    []Slot
}

type Event struct {
	Time     float64
	Statu    string
	Info     string
	Value    int64
}

type Storage struct {
	Map   map[int]Event
	Lock  *sync.Mutex
}