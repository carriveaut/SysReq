import django_tables2 as tables
from .models import Ticket


ticket_date = ''' <div class="dateSquare">
                    <h3>MAR</h3>
                    <h3>10</h3>
                    <h3>2018</h3>
                  </div> '''

add_ticket = '''<a href="{% url 'Tickets:viewticket' %}" role="button" 
                class="btn btn-secondary" id="ticketid" >View Ticket</a>'''


class TicketTable(tables.Table):
    date = tables.TemplateColumn(ticket_date, verbose_name=" ", orderable=False)
    add = tables.TemplateColumn(add_ticket, verbose_name=" ", orderable=False)
    id =  tables.Column(visible=False)
    classification = tables.Column(visible=False)
    start_Date = tables.Column(visible=False)
    status = tables.Column(visible=False)
    event = tables.Column(" ", orderable=False)
    venues = tables.Column(" ", orderable=False)
    start_Time = tables.Column(" ", orderable=False)
    class Meta:
        model = Ticket
        sequence = ('date', 'event', 'venues', 'start_Time', 'add')
        attrs = {'class': 'ticket'}
