package main

import (
	"strconv"
	"strings"
)

func Factory(text string) Event {
	var segs []string
	pieces := strings.Split(text, " ")
	for _, piece := range pieces {
		if piece != "" {
			segs = append(segs, piece)
		}
	}

	newEvent := Event{
		Statu: segs[3],
		Info:  segs[4],
	}
	if segs[5] == "DOWN" {
		newEvent.Value = -333 // Down
	} else if segs[5] == "UP" {
		newEvent.Value = -444 // Up
	} else if segs[5] == "ffffffff" {
		newEvent.Value = -1 // -1, means that's track is done
	} else {
		num, err := strconv.ParseInt(segs[5], 16, 32)
		if err != nil {
			panic(err)
		}
		newEvent.Value = num
	}

	newEvent.Time, _ = strconv.ParseFloat(strings.TrimRight(segs[1], "]"), 64)
	return newEvent
}
