from main_app.models import Donation


def get_bags_quantity():
    donations = Donation.objects.all()
    bags_quantity = 0
    for donation in donations:
        bags_quantity += donation.quantity
    return bags_quantity


def get_supported_institutions_amount():
    donations = Donation.objects.all()
    supported_institutions = []
    for donation in donations:
        if donation.institution.name not in supported_institutions:
            supported_institutions.append(donation.institution.name)
    return len(supported_institutions)
