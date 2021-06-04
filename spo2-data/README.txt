The files in this directory contain sample PPG data, obtained from one subject.
All data was collected while the subject was seated and at rest.

1) FOLDER 'proto1' - eval kit
  Low SpO2 levels were induced using the Hypoxico High Altitude Training System.
  Data was gathered with a finger placed on the sensor, using the MAXIM86161 eval kit.
  Each file is one test point, including only a few seconds of data.
  
  The file names indicate the reference SpO2 and heart rate readings for that test point,
    in the following format:
      "<time>-<SpO2 reading>-<heart rate reading>.csv"
	So, "1410-95-79.csv" indicates a Spo2 reading of 95 and a heart rate of 79.

  FILE FORMAT: The file is a comma-separated-value (.csv) file, starting with several rows
    of header information.  The PPG data is in columns:
      LEDC1: Infrared LED signal
      LEDC2: Red LED signal
      LEDC3: Ambient light signal (photo sensor reading with no LEDs lit)
    Each signal is sampled at 64 Hz.

2) FOLDER 'proto2' - our prototype
  Data was gathered using our prototype OxiWear device attached to the ear.
  Data was transmitted over Bluetooth Low Energy (BLE) to our recording software.
  Reference readings were taken visually from a finger-attached pulse-oximeter and recorded manually.

  File names have the following format:
    "<date>-<time>-<SpO2 range>-<heart rate range>-<notes>.csv"
      SpO2 and HR readings are not necessarily constant throughout each test.
      Where they varied, a range was recorded:
    "20201012-165638-9596-7174.csv" means Spo2 varied between 95 and 96, and HR between 71 and 74.

  FILE FORMAT: A .csv file, with one header row, and the PPG data in columns:
    1: IR LED signal
    2: ambient light signal
    3: Red LED signal
    *** Each signal is sampled at 24.995 Hz ***

