package main

import (
	"fmt"
	"os"
	"bufio"
	"sync"
	"strings"
	"strconv"
)

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

func main() {
	fmt.Println("[Running...]")

	file, err := os.Open("out.txt")
	if err != nil {
		fmt.Printf("[Error]: %s\n", err)
	}
	defer file.Close()

	store := Storage{
		Map: make(map[int]Event),
		Lock: new(sync.Mutex),
	}
	var wg sync.WaitGroup

	counter := 0
	scanner := bufio.NewScanner(file)
	
	for scanner.Scan() {
		counter += 1
		wg.Add(1)

		go func(id int, text string) {
			defer wg.Done()

			if strings.HasPrefix(text, "[") {
				var segs []string
				pieces := strings.Split(text, " ")
				for _, piece := range pieces {
					if piece != "" {
						segs = append(segs, piece)	
					}
				}

				newEvent := Event {
					Statu: segs[3],
					Info: segs[4],
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
				
				store.Lock.Lock()
				store.Map[id] = newEvent
				store.Lock.Unlock()
			}
		}(counter, scanner.Text())
	}

	wg.Wait()
	fmt.Println("[Analysing...]")

// Now obey the MIT TypeB protocol...

	collection := Collection{
		Slots: make([]Slot, 5),
	}
	slotNow := 0
	collection.Slots[0] = Slot {
		Tracks: make([]Track),
		Used: true,
	}
	var trackNow Track
	posNow := make([]Position, 5)
	widthNow := make([]int64, 5)
	for i:=1; i<=counter; i++ {
		eventNow := store.Map[i].Statu

        if eventNow.Statu == "EV_ABS" {
        	if eventNow.Info == " ABS_MT_TRACKING_ID" {
        		if eventNow.Value == -1 {
        			if i<counter || store.Map[i+1].Statu == "EV_KEY" {
        				// the up action
        				trackNow.Reports = append(trackNow.Reports, Report {
        					Time: store.Map[i+1].Time,
        					IsBtn: true,
        				})
        			}

        			collection.Slots[slotNow].Tracks = append(collection.Slots[slotNow].Tracks, trackNow)
        			// close the slot here
        			posNow[slotNow] = Position{}
        			widthNow[slotNow] = 0
        		} else {
        			trackNow := Track{
        				ID: eventNow.Value,
        				Reports: make([]Report),
        			}
        		}
        	} else if eventNow.Info == "ABS_MT_SLOT" {
        		// update the slot
        		if slotNow != eventNow.Value {
        			slotNow = eventNow.Value
        		}

        		// init new slot
        		if !collection.Slots[slotNow].Used {
        			collection.Slots[slotNow] = Slot {
        				Used: true,
        				Tracks: make([]Track),
        			}
        		}
        	} else if eventNow.Info == "ABS_MT_POSITION_X" {
        		posNow[slotNow].X = eventNow.Value
        	} else if eventNow.Info == "ABS_MT_POSITION_Y" {
        		posNow[slotNow].Y = eventNow.Value
        	} else if eventNow.Info == "ABS_MT_WIDTH_MAJOR" {
        		widthNow[slotNow] = eventNow.Value
        	}
        } else { // EV_SYN
        	if i > 1 && strings.HasPrefix(store.Map[i-1].Info, "ABS_MT_POSITION_") {
        		// report the position
        		trackNow.Reports = append(trackNow.Reports, Report {
        			Time: store.Map[i-1].Time,
        			IsBtn: false,
        			Pos: Position {
        				X: posNow[slotNow].X,
        				Y: posNow[slotNow].Y,
        			},
        			Width: widthNow[slotNow],
        		})
        	}
        }
	}
	
	return
}