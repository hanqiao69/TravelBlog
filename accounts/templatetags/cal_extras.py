from django.template import Library

register = Library()
@register.filter(name="iconclass")
def iconclass(wetdry):
  if wetdry == "Rainy":
    return "umbrella"
  elif wetdry == "Dry":
    return "sun-o"
@register.filter(name='format_percentage')
def format_perc(value):
  if value:
    return abs(value)*100
  else:
    return value
@register.filter(name='format_percentage_signed')
def format_perc_signed(value):
  if value:
    return (value)*100
  else:
    return value
@register.filter(name='thumb')
def thumb(value):
    return "images/Thumb"+value
@register.filter(name='better_worse')
def better_worse(value):
    if value < 0:
      return "worse"
    else:
      return "better"
@register.filter
def modulo(num, val):
    return num % val
@register.filter(name='value_percentage')
def val_perc(value):
    if not value:
      return "N/A"
    if value < -0.01:
      return "Poor"
    elif value < 0.01:
      return "So-So"
    elif value < 0.1:
      return "Good"
    elif value < 0.2:
      return "Great"
    else:
      return "Spectacular"
@register.filter
def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range( value )
@register.filter(name='num')
def num(value, arg):
    return int(arg)*48 + int(value)+1
@register.filter(name='divideby')
def divideby(value, arg):
    return int(value)/arg
@register.filter(name='even')
def divide(value):
    return int(value)%2==0
@register.filter(name='evenstring')
def evenstring(value):
    return "even" if (int(value)%2==0) else "odd"
@register.filter(name='totime')
def totime(value):
    array = ["Midnight", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "Noon", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM", "Midnight"]
    return array[value]
@register.filter(name='day')
def day(value):
    array = ["","Sun.", "Mon.", "Tues.", "Wed.", "Thurs.", "Fri.", "Sat."]
    return array[value]
@register.filter(name='highlight')
def base_cal(value, arg):
    print value
    if(arg==None):
      return ""
    if(arg[value-1]=="1"):
        return "highlighted"
    else:
        return ""
@register.filter(name='truefalse')
def base_cal(value, arg):
    print value
    if(arg==None):
      return "false"
    if(arg[value-1]=="1"):
        return "true"
    else:
        return "false"