import os
import random
from datetime import *
from pathlib import Path


# --------------------- encrypt ---------------------
def create_xml(
    length: int,
    material: str,
    project_name: str,
    element_name: str,
    profile: str,
    user: str,
):
    profile_dir = Path(__file__).resolve().parent
    profile_dir = os.path.join(profile_dir, "profiles/")

    current_time = datetime.now()
    project_name = str(project_name)
    element_name = str(element_name)
    material = str(material)
    profile_length = str(length)
    detail_id = int(1)
    detail_beam_id = int(1)

    year = "{:02d}".format(current_time.year)
    month = "{:02d}".format(current_time.month)
    day = "{:02d}".format(current_time.day)
    ymd = "{}-{}-{}".format(year, month, day)
    hour = "{:02d}".format(current_time.hour)
    minute = "{:02d}".format(current_time.minute)
    second = "{:02d}".format(current_time.second)
    hms = "{}:{}:{}".format(hour, minute, second)
    hms_n = "{}-{}-{}".format(hour, minute, second)

    file_name = str(f"{project_name}_{element_name}_{user}_{hms_n}")

    f = open(profile_dir.replace("\\", "/") + file_name + ".xml", "w")
    f.write('<?xml version="1.0" encoding="utf-8"?>')
    f.write("\n\n")
    f.write("<BatchDataSet>")
    f.write("\n")
    f.write("<Meta>")
    f.write("\n")
    f.write("  <CreationTime>")
    f.write(str(ymd))
    f.write("T" + str(hms) + "." + str(current_time.microsecond) + "+03:00")
    f.write("</CreationTime>")
    f.write("\n")
    f.write("  <CreatedBy />")
    f.write("\n")
    f.write("  <ModificationTime>")
    f.write(str(ymd))
    f.write("T" + str(hms) + "." + str(current_time.microsecond) + "+03:00")
    f.write("</ModificationTime>")
    f.write("\n")
    f.write("  <ModificatedBy>not modified</ModificatedBy>")
    f.write("\n")
    f.write("  <Version>1.0</Version>")
    f.write("\n")
    f.write("  <CadVersion>20.0 Service Release 5</CadVersion>")
    f.write("\n")
    f.write("  </Meta>")
    f.write("\n\n")

    f.write("<Project>")
    f.write("\n")
    f.write("  <ProjectID>1</ProjectID>")
    f.write("\n")
    f.write("  <ProjectName>")
    f.write(str(project_name))
    f.write("</ProjectName>")
    f.write("\n")
    f.write("  </Project>")
    f.write("\n\n")

    f.write("<Element>")
    f.write("\n")
    f.write("  <ElementID>1</ElementID>")
    f.write("\n")

    f.write("  <ElementProjectID>1</ElementProjectID>")
    f.write("\n")
    f.write("  <ElementName>")
    f.write(str(element_name))
    f.write("</ElementName>")
    f.write("\n")
    f.write("  <ElementTypeStr>wall</ElementTypeStr>")
    f.write("\n")
    f.write("  <ElementFilePath>")
    f.write(str("C:\ConstructFiles"))
    f.write("</ElementFilePath>")
    f.write("\n")
    f.write("  <ElementCount>1</ElementCount>")
    f.write("\n")
    f.write("</Element>")
    f.write("\n\n")

    f.write("<Beam>")
    f.write("\n")
    f.write("  <BeamID>1</BeamID>")
    f.write("\n")
    f.write("  <BeamElementID>1</BeamElementID>")
    f.write("\n")
    f.write("  <BeamSerial>")
    f.write(str(int(random.uniform(1, 1000000))))
    f.write("</BeamSerial>")
    f.write("\n")
    f.write("  <BeamName>")
    f.write(str(profile))
    f.write("</BeamName>")
    f.write("\n")
    f.write("  <BeamMaterialGrade>")
    f.write(str(material))
    f.write("</BeamMaterialGrade>")
    f.write("\n")
    f.write("  <BeamRotation>90</BeamRotation>")
    f.write("\n")

    f.write("  <BeamXStart>0</BeamXStart>")
    f.write("\n")
    f.write("  <BeamYStart>0</BeamYStart>")
    f.write("\n")
    f.write("  <BeamZStart>0</BeamZStart>")
    f.write("\n")

    f.write("  <BeamXEnd>")
    f.write(str(profile_length))
    f.write("</BeamXEnd>")
    f.write("\n")
    f.write("  <BeamYEnd>0</BeamYEnd>")
    f.write("\n")
    f.write("  <BeamZEnd>0</BeamZEnd>")
    f.write("\n")

    f.write("  <BeamLength>")
    f.write(str(profile_length))
    f.write("</BeamLength>")
    f.write("\n")
    f.write("</Beam>")
    f.write("\n\n")

    f.write("<Detail>")
    f.write("\n")
    f.write("  <DetailID>")
    f.write(str(detail_id))
    detail_id = detail_id + 1
    f.write("</DetailID>")
    f.write("\n")
    f.write("  <DetailBeamID>")
    f.write(str(detail_beam_id))
    f.write("</DetailBeamID>")
    f.write("\n")
    f.write("  <DetailType>Front</DetailType>")
    f.write("\n")
    f.write("  <DetailName>Straight</DetailName>")
    f.write("\n")
    f.write("  <DetailXPos>0</DetailXPos>")
    f.write("\n")
    f.write("  <DetailYPos>0</DetailYPos>")
    f.write("\n")
    f.write("  <DetailProfileFace>Web</DetailProfileFace>")
    f.write("\n")
    f.write("  </Detail>")
    f.write("\n\n")

    f.write("<Detail>")
    f.write("\n")
    f.write("  <DetailID>")
    f.write(str(detail_id))
    f.write("</DetailID>")
    f.write("\n")
    f.write("  <DetailBeamID>")
    f.write(str(detail_beam_id))
    f.write("</DetailBeamID>")
    f.write("\n")
    f.write("  <DetailType>End</DetailType>")
    f.write("\n")
    f.write("  <DetailName>Straight</DetailName>")
    f.write("\n")
    f.write("  <DetailXPos>0</DetailXPos>")
    f.write("\n")
    f.write("  <DetailYPos>0</DetailYPos>")
    f.write("\n")
    f.write("  <DetailProfileFace>Web</DetailProfileFace>")
    f.write("\n")
    f.write("  </Detail>")
    f.write("\n\n")

    f.write("</BatchDataSet>")
    f.close()

    return {
        "path": str(profile_dir.replace("/", "\\") + file_name + ".xml"),
        "name": str(file_name + ".xml"),
    }
