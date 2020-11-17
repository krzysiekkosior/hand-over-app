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


def get_donation_list(user):
    donations = Donation.objects.filter(user=user)
    taken_donations = []
    not_taken_donations = []

    for donation in donations:
        if donation.is_taken is True:
            taken_donations.append(donation)
        else:
            not_taken_donations.append(donation)
    not_taken_donations_amount = len(not_taken_donations)
    return taken_donations, not_taken_donations, not_taken_donations_amount


def change_donation_status_to_taken(id_list):
    for donation_id in id_list:
        donation = Donation.objects.get(id=int(donation_id))
        donation.is_taken = True
        donation.save()
