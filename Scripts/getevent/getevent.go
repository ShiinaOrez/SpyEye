package main

import (
    "bufio"
    "fmt"
    "os/exec"
    "os"
    "time"
)

func main() {
	start := time.Now()
    cmd := exec.Command("adb", "shell", "getevent", "-lt")

	file, err := os.OpenFile("out.txt", os.O_WRONLY|os.O_APPEND, 0644)
	defer file.Close()

    stdout, err := cmd.StdoutPipe()
    if err != nil {
        fmt.Printf("Error:can not obtain stdout pipe for command:%s\n", err)
        return
    }
    if err := cmd.Start(); err != nil {
        fmt.Println("Error:The command is err,", err)
        return
    }
 
    outputBuf := bufio.NewReaderSize(stdout, 128)
    errChan := make(chan error)
    count := 0

    go func() {
    	for {
    		output, _, _ := outputBuf.ReadLine()
    		file.Write(append(output, '\n'))
    		go func() {
    			count += 1
    			fmt.Printf("%s Now: %d\r", fmtDuration(time.Since(start)), count)
    		}()
    	}
    }()

    var str string
    fmt.Scanln(&str)
    return

	errChan <-cmd.Wait()
    if <-errChan != nil {
  		return
 	}
 	return
}

func fmtDuration(d time.Duration) string {
    d = d.Round(time.Second)
    h := d / time.Hour
    d -= h * time.Hour
    m := d / time.Minute
    d -= m * time.Minute
    s := d / time.Second
    return fmt.Sprintf("%02d:%02d:%02d", h, m, s)
}