package main

import (
    "context"
    "log"
    "strings"
    "os"
    "os/signal"
    "syscall"

    ParsRubika "github.com/AbolfazlZarei-dev/ParsRubika-bot-go/v2"
)

func main() {
    token := "BEHFJF0YAIALQLLOIEKEEMMOFWIJHEGGLPPEHZPXDPABVDUABKUXBJNAOOCFYHXL"

    bot := ParsRubika.NewClient(token)

    // هندلر پیام‌ها
    bot.OnMessageUpdates(func(ctx context.Context, update *ParsRubika.Update) error {
        if update.NewMessage != nil && update.NewMessage.Text != "" {
            text := strings.TrimSpace(update.NewMessage.Text)
            
            if text == "/start" {
                bot.SendMessage(ctx, &ParsRubika.SendMessageRequest{
                    ChatID: update.ChatID,
                    Text:   "سلام! 🌟\nربات من با Go روشن شد!",
                })
            } else if strings.HasPrefix(text, "/") {
                bot.SendMessage(ctx, &ParsRubika.SendMessageRequest{
                    ChatID: update.ChatID,
                    Text:   "دستور نامعتبر!\nبرای راهنما /start رو بفرست.",
                })
            } else {
                bot.SendMessage(ctx, &ParsRubika.SendMessageRequest{
                    ChatID: update.ChatID,
                    Text:   "شما گفتید: " + text,
                })
            }
        }
        return nil
    })

    ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
    defer stop()

    log.Println("🤖 ربات روبیکا با Go روشن شد!")
    if err := bot.Run(ctx); err != nil {
        log.Fatal("خطا:", err)
    }
}
