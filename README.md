# EB-ShipStation_PubRates

This script uses Shipstations API to return the published shipping rates of orders provided.

Needed Python Libraries: Pandas

1. download the data from shipstation
   Shipstation.com > Insights > Reports > (Scroll to bottom) Raw Data Exports > Shipped Orders

2. Name csv file: EB-ShipStation.csv and place in folder with this script.

3. Run script to return new dataset called "ShipStationPubRates.csv" in same directory

4. compare columns "Carrier fee" and new column "Rates" and make sure Rates are a larger value.

5. remove "carrier Fee" column
