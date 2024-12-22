import pandas as pd
import streamlit as st
import time
import matplotlib.pyplot as plt
import gc

st.title("Visualisasi Sorting dan Kompleksitas Waktu")

file_path = "penjualan.xlsx"

try:
    data = pd.read_excel(file_path)
    st.success(f"File '{file_path}' berhasil dibaca!")

    st.subheader("Data yang Diimpor")
    st.dataframe(data)

    if "penjualan" not in data.columns or "nama_produk" not in data.columns:
        st.error("Kolom 'penjualan' atau 'nama_produk' tidak ditemukan.")
    elif not pd.api.types.is_numeric_dtype(data["penjualan"]):
        st.error("Kolom 'penjualan' harus berupa angka.")
    else:
        sales_data = data["penjualan"].tolist()
        produk_data = data["nama_produk"].tolist()

        combined_data = list(zip(produk_data, sales_data))

        def selection_sort(arr):
            arr = arr.copy()  
            n = len(arr)
            for i in range(n):
                min_idx = i
                for j in range(i + 1, n):
                    if arr[j][1] > arr[min_idx][1]:
                        min_idx = j
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
            return arr

        def rec_merge_sort(arr):
            if len(arr) <= 1:
                return arr
            middle = len(arr) // 2
            left = rec_merge_sort(arr[:middle])
            right = rec_merge_sort(arr[middle:])
            return merge(left, right)

        def merge(left, right):
            if not left:
                return right
            if not right:
                return left
            if left[0][1] > right[0][1]:
                return [left[0]] + merge(left[1:], right)
            else:
                return [right[0]] + merge(left, right[1:])

        def ukur_waktu_rata2(algoritma, data, iterasi=5):
            total_time = 0
            for _ in range(iterasi):
                gc.collect() 
                start_time = time.time()
                algoritma(data.copy())
                total_time += time.time() - start_time
            return total_time / iterasi

        def perbandingan_efisiensi():
            sizes = [10, 50, 100, 500, 1000]  
            waktu_selection = []
            waktu_merge = []
            tabel_waktu = []

            for size in sizes:
              
                subset_data = combined_data[:size]
                
               
                waktu_selection_avg = ukur_waktu_rata2(selection_sort, subset_data)
                waktu_selection.append(waktu_selection_avg)
                
             
                waktu_merge_avg = ukur_waktu_rata2(rec_merge_sort, subset_data)
                waktu_merge.append(waktu_merge_avg)
                
               
                tabel_waktu.append([size, waktu_selection_avg, waktu_merge_avg])

           
            st.subheader("Perbandingan Waktu Eksekusi Berdasarkan Ukuran Data")
            fig, ax = plt.subplots()
            ax.plot(sizes, waktu_selection, label="Selection Sort", color="blue", marker='o')
            ax.plot(sizes, waktu_merge, label="Merge Sort", color="green", marker='o')
            ax.set_xlabel("Ukuran Data")
            ax.set_ylabel("Waktu (detik)")
            ax.set_title("Perbandingan Waktu Eksekusi: Selection Sort vs Merge Sort")
            ax.legend()
            st.pyplot(fig)

           
            st.subheader("Tabel Perubahan Running Time")
            df_tabel_waktu = pd.DataFrame(tabel_waktu, columns=["Input Size (n)", "Selection Sort Time (T(n))", "Merge Sort Time (T(n))"])
            st.dataframe(df_tabel_waktu)

        perbandingan_efisiensi()

        sorted_selection = selection_sort(combined_data.copy())
        sorted_rec_merge_sort = rec_merge_sort(combined_data.copy())

        st.subheader("Hasil Sorting")

        st.write("Selection Sort", pd.DataFrame(sorted_selection, columns=["Nama Produk", "Penjualan"]))

        st.write("Merge Rekursif", pd.DataFrame(sorted_rec_merge_sort, columns=["Nama Produk", "Penjualan"]))

        st.subheader("Grafik Hasil Sorting Selection Sort (Descending)")
        fig3, ax3 = plt.subplots()
        nama_produk_sorted_selection = [item[0] for item in sorted_selection]
        penjualan_sorted_selection = [item[1] for item in sorted_selection]
        ax3.bar(nama_produk_sorted_selection, penjualan_sorted_selection, color="purple")
        ax3.set_ylabel("Penjualan")
        ax3.set_title("Hasil Sorting Ascending Berdasarkan Penjualan (Selection Sort)")
        plt.xticks(rotation=90)
        st.pyplot(fig3)

        st.subheader("Grafik Hasil Sorting Merge Sort Rekursif (Descending)")
        fig4, ax4 = plt.subplots()
        nama_produk_sorted_rec_merge_sort = [item[0] for item in sorted_rec_merge_sort]
        penjualan_sorted_rec_merge_sort = [item[1] for item in sorted_rec_merge_sort]
        ax4.bar(nama_produk_sorted_rec_merge_sort, penjualan_sorted_rec_merge_sort, color="orange")
        ax4.set_ylabel("Penjualan")
        ax4.set_title("Hasil Sorting Descending Berdasarkan Penjualan (Merge Sort Rekursif)")
        plt.xticks(rotation=90)
        st.pyplot(fig4)

        waktu_selection_total = ukur_waktu_rata2(selection_sort, combined_data.copy())
        waktu_rec_merge_sort_total = ukur_waktu_rata2(rec_merge_sort, combined_data.copy())
        
        st.write(f"**Selection Sort:** {waktu_selection_total:.6f} detik")
        st.write(f"**Rekursif Merge Sort:** {waktu_rec_merge_sort_total:.6f} detik")
        st.write(f"**Perbedaan Running Time:** {abs(waktu_selection_total - waktu_rec_merge_sort_total):.6f} detik")

except FileNotFoundError:
    st.error(f"File '{file_path}' tidak ditemukan.")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
