package main

import (
    "context"
    "log"
    "os"
    "os/signal"
    "syscall"

    ParsRubika "github.com/AbolfazlZarei-dev/ParsRubika-bot-go/v2"
)

func main() {
    // توکن ربات خود را وارد کنید
    token := "BEHFJF0YAIALQLLOIEKEEMMOFWIJHEGGLPPEHZPXDPABVDUABKUXBJNAOOCFYHXL"

    // ایجاد کلاینت جدید
    bot := ParsRubika.NewClient(token)

    // هندلر برای پیام‌های متنی
    bot.OnMessageUpdates(func(ctx context.Context, update *ParsRubika.Update) error {
        if update.NewMessage != nil && update.NewMessage.Text != "" {
            text := update.NewMessage.Text
            
            if text == "/start" {
                _, err := bot.SendMessage(ctx, &ParsRubika.SendMessageRequest{
                    ChatID: update.ChatID,
                    Text:   "سلام! 🤖\nربات من با موفقیت در Go روشن شد!",
                })
                return err
            } else {
                _, err := bot.SendMessage(ctx, &ParsRubika.SendMessageRequest{
                    ChatID: update.ChatID,
                    Text:   "شما گفتید: " + text,
                })
                return err
            }
        }
        return nil
    })

    // تنظیم قطع شدن برنامه با سیگنال
    ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
    defer stop()

    log.Println("🤖 ربات Go در حال اجراست...")
    if err := bot.Run(ctx); err != nil {
        log.Fatal("خطا در اجرای ربات:", err)
    }
}
