# PDF Conference Tool - Automate Certificate Generation with Python, Flask, pandas, and pdfrw
Welcome to the PDF Conference Tool, a powerful solution designed to streamline the process of creating PDF certificates for conferences or workshops. With this web application, you can effortlessly fill PDF certificates with data from an Excel table, saving you time and effort. Watch the video demo here to see the tool in action: <https://www.youtube.com/watch?v=e8qH6gDhkPU>
Access the website here: https://pdffill.pythonanywhere.com/
![pdffill](https://github.com/Curiosit/pdf-conference-tool/assets/17218693/11193240-659f-40f6-8c89-df56eba6e7c7)

### Tech Stack
This project is developed using Python, leveraging the Flask framework, along with pandas for data manipulation and pdfrw for PDF processing.

### Description
Generating numerous PDF certificates for a conference or workshop can be a challenging task. However, our PDF Conference Tool simplifies this process. By uploading a properly formatted PDF and an Excel table, you can automatically populate the PDF certificates with the required data. Say goodbye to manual data entry and hello to efficiency!

### Template Files
Explore the 'static' folder, which contains essential template files. The Excel file, named 'example_data.xls,' and the PDF template, 'temp.pdf,' are customizable. Feel free to modify these files to achieve different results according to your specific needs.

### File Structure
The core logic of the application resides in 'app.py.' Additionally, you'll find various layout files in the 'static' folder, allowing for flexibility in the presentation of your certificates.

### Application Logic
Here's a breakdown of the application's workflow:

- **Excel File Submission**: When a user submits an Excel file, the application reads it into a pandas dataframe, providing a structured representation of the data.

- **PDF Generation**: The template PDF is opened, and a copy is generated for each row in the dataframe. All fillable form fields in the PDF are populated with data from the dataframe.

- **PDF Merging**: The individual PDFs are then merged into a single file, ensuring a consolidated document for easier distribution.

- **Temporary PDF Creation**: Using 'io.BytesIO()', a temporary PDF file is created. Subsequently, the file is reopened to modify the 'NeedAppearances' attribute (set to pdfrw.PdfObject("true")). This step is crucial to ensure form visibility on all devices.

- **File Delivery**: The modified file is then written and sent as an attachment to the user, providing a seamless and automated certificate generation process.

Experience the convenience of our PDF Conference Tool today and revolutionize the way you handle certificate creation for your events!
