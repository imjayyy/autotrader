import pandas as pd
from auction.models import AuctionCompany, ShippingCompany


def update_model_from_csv(filename, model):

    model_df = pd.read_csv(filename)
    model_df.fillna('', inplace=True)

    if "cities.csv" in filename:
        model_df['Name'] = model_df['Name'].str.slice(4)

    for i in range(len(model_df.index)):
        model_data = model_df.loc[i].to_dict()

        if "auction_shipping.csv" in filename:
            model_data.update(AuctionCompanyId=AuctionCompany.objects.get(Id=model_data['AuctionCompanyId']), ShippingCompanyId=ShippingCompany.objects.get(Id=model_data['ShippingCompanyId']))

        model.objects.create(**model_data)
