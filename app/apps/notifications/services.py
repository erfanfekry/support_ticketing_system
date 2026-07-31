from django.core.mail import send_mail

class NotificationService: 
    @classmethod
    def ticket_message_created(cls, ticket, message, sender):
        
        new_ticket_notification_message = 40 * '*' + '\n' \
                                          f'A new message was created in ticket_id = {ticket.id} with following info:\n' \
                                          f'sender:{sender}\n' \
                                          f'message:{message.message}\n' \
                                          f'create at: {message.created_at}\n' + \
                                          40 * '*'
        # SMS Notification
        print('SMS:\n', new_ticket_notification_message)

        # Email Notification
        send_mail(subject='New ticket message.',
                  message='Email:\n' + new_ticket_notification_message, 
                  from_email='erfanfekry@gmail.com',
                  recipient_list=[ticket.order.customer.email],
                  fail_silently=False )
