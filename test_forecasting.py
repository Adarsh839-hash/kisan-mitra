from src.data_loader import load_mandi_data
from src.forecasting import predict_kisan_mitra

mandi_all, batch_data = load_mandi_data()

result = predict_kisan_mitra(
    commodity="Wheat",
    market="Bhikangaon APMC",
    data=batch_data
)

print(result)