import pandas as pd
import streamlit as st

class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

class Course:
    def __init__(self, course_code, course_name):
        self.course_code = course_code
        self.course_name = course_name

class Grade:
    def __init__(self, student, course, score):
        self.student = student
        self.course = course
        self.score = score

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.data = []  # Menyimpan nilai-nilai (objek Grade) dengan kunci ini
        self.left = None
        self.right = None

class GradeBST:
    def __init__(self):
        self.root = None

    def insert(self, key, grade):
        self.root = self._insert(self.root, key, grade)

    def _insert(self, root, key, grade):
        if root is None:
            new_node = TreeNode(key)
            new_node.data.append(grade)
            return new_node

        if key < root.key:
            root.left = self._insert(root.left, key, grade)
        elif key > root.key:
            root.right = self._insert(root.right, key, grade)
        else:
            # Jika kunci sudah ada, tambahkan nilai ke dalam data
            root.data.append(grade)

        return root

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, root, key):
        if root is None or root.key == key:
            return root.data
        if key < root.key:
            return self._search(root.left, key)
        return self._search(root.right, key)

    def inorder_traversal(self, root=None):
        if root is None:
            root = self.root
        result = []
        self._inorder_traversal(root, result)
        return result

    def _inorder_traversal(self, root, result):
        if root:
            self._inorder_traversal(root.left, result)
            result.extend(root.data)
            self._inorder_traversal(root.right, result)

    def save_to_csv(self, file_path):
        inorder_result = self.inorder_traversal()
        data_list = []
        for grade in inorder_result:
            data_list.append({
                'StudentID': grade.student.student_id,
                'Student Name': grade.student.name,
                'CourseCode': grade.course.course_code,
                'CourseName': grade.course.course_name,
                'Score': grade.score
            })
        data_frame = pd.DataFrame(data_list)
        data_frame.to_csv(file_path, index=False)

def import_data(file_path):
    try:
        # Membaca data dari file CSV
        data_frame = pd.read_csv(file_path)
        return data_frame
    except FileNotFoundError:
        st.error(f"File {file_path} tidak ditemukan.")
        return None
    except Exception as e:
        st.error(f"Terjadi kesalahan saat mengimpor data: {str(e)}")
        return None

def main():
    # Membuat objek BST
    grade_bst = GradeBST()

    # Nama file CSV dan kolom-kolom
    file_path = 'file.csv'
    student_id_column = 'StudentID'
    student_name_column = 'Student Name'
    course_code_column = 'CourseCode'
    course_name_column = 'CourseName'
    score_column = 'Score'

    # Memanggil fungsi import_data
    imported_data = import_data(file_path)

    # Menampilkan data (opsional)
    if imported_data is not None:
        st.title("Data Nilai Mahasiswa")

        # Menampilkan data yang diimpor
        st.subheader("Data yang diimpor:")
        st.write(imported_data)

        # Mengimpor data ke dalam BST
        for index, row in imported_data.iterrows():
            student_id = row[student_id_column]
            grade = Grade(
                Student(student_id, row[student_name_column]),
                Course(row[course_code_column], row[course_name_column]),
                row[score_column]
            )
            grade_bst.insert(student_id, grade)

        # Menampilkan data BST
        st.subheader("Data pada Binary Search Tree:")
        inorder_result = grade_bst.inorder_traversal()
        for grade in inorder_result:
            st.write(
                f"ID Mahasiswa: {grade.student.student_id}, Nama Mahasiswa: {grade.student.name}, "
                f"Kode Mata Kuliah: {grade.course.course_code}, Nama Mata Kuliah: {grade.course.course_name}, "
                f"Nilai: {grade.score}",
            )

        # Menu Tambah Data
        st.subheader("Tambah Data:")
        new_student_id = st.number_input("ID Mahasiswa", min_value=1)
        new_student_name = st.text_input("Nama Mahasiswa")
        new_course_code = st.text_input("Kode Mata Kuliah")
        new_course_name = st.text_input("Nama Mata Kuliah")
        new_score = st.number_input("Nilai", min_value=0, max_value=100)

        if st.button("Tambah"):
            new_grade = Grade(
                Student(new_student_id, new_student_name),
                Course(new_course_code, new_course_name),
                new_score
            )
            grade_bst.insert(new_student_id, new_grade)
            st.success("Data berhasil ditambahkan.")
            # Simpan kembali ke file CSV setelah menambah data baru
            grade_bst.save_to_csv(file_path)

        # Menu Hapus Data
        st.subheader("Hapus Data:")
        delete_student_id = st.number_input("ID Mahasiswa yang akan dihapus", min_value=1)
        if st.button("Hapus"):
            deleted_data = grade_bst.search(delete_student_id)
            if deleted_data:
                grade_bst.root = None  # Reset BST
                for data in inorder_result:
                    if data.student.student_id != delete_student_id:
                        grade_bst.insert(data.student.student_id, data)
                st.success(f"Data Mahasiswa ID {delete_student_id} berhasil dihapus.")
                # Simpan kembali ke file CSV setelah menghapus data
                grade_bst.save_to_csv(file_path)
            else:
                st.warning(f"Data Mahasiswa ID {delete_student_id} tidak ditemukan.")

        # Menu Lihat Data
        st.subheader("Lihat Data:")
        st.write("Pilih ID Mahasiswa untuk melihat data:")
        selected_student_id = st.selectbox("ID Mahasiswa", sorted(set(imported_data[student_id_column])))
        selected_data = grade_bst.search(selected_student_id)
        if selected_data:
            st.write(f"Data Mahasiswa ID {selected_student_id}:")
            for data in selected_data:
                st.write(
                    f"Nama Mahasiswa : {grade.student.name}  \n",
                    f"Kode Mata Kuliah: {data.course.course_code}  \n Nama Mata Kuliah: {data.course.course_name}  \n "
                    f"Nilai: {data.score}  \n"
                )
        else:
            st.warning(f"Data Mahasiswa ID {selected_student_id} tidak ditemukan.")

if __name__ == "__main__":
    main()
