from flask import flash
from wtforms.validators import ValidationError

def flash_errors(form):
    """
    Flashes form errors
    """
    for _, errors in form.errors.items():
        for error in errors:
            flash( (error), 'error')

class Compare(object):  # --> Change to 'LessThan'
    """
    Compares the values of two fields.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """
    def __init__(self, fieldname, message=None, direction="left"):
        self.fieldname = fieldname
        self.message = message
        self.direction = direction

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if self.direction=="left":
            validate=field.data>other.data
        elif self.direction=="right":
            validate=field.data<other.data
        elif self.direction=="equal":
            validate=field.data==other.data
        else:
            raise ValidationError("Direction not defined")
        if not validate:  #  --> Change to >= from !=
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                message = field.gettext('Validation Failed.')

            raise ValidationError(message % d)