import base64
import os
import zlib
from enum import Enum
from typing import List, Tuple, Optional, Union

import numpy as np
import tqdm
from lxml import etree

cv_count = 0


def echo_processor(line: str, events):
    global current_processor
    events = iter(events)
    for action, elem in events:
        if action == 'start' and elem.tag == '{http://psi.hupo.org/ms/mzml}cvList':
            current_processor = cv_processor
            current_processor(line, events)
            break
        else:
            print(line.rstrip())


def cv_processor(line: str, events):
    global current_processor
    global cv_count

    events = iter(events)
    for action, elem in events:
        if action == 'start' and elem.tag == '{http://psi.hupo.org/ms/mzml}cv':
            cv_count += 1
        elif action == 'end' and elem.tag == '{http://psi.hupo.org/ms/mzml}cvList':
            print('## cv_count: {}'.format(cv_count))
            current_processor = echo_processor
            break


current_processor = echo_processor

ns = {'ns': 'http://psi.hupo.org/ms/mzml'}


def xpath(element: etree._Element, xpath: str) -> List[Union[etree._Element, str]]:
    return element.xpath(xpath, namespaces=ns)


def attr(element: etree._Element, xpath: str) -> Optional[str]:
    res = element.xpath(xpath + '/@value', namespaces=ns)
    if res:
        return res[0]
    else:
        return None


class DataKind(Enum):
    mz = 0
    intensity = 1


class Precision(Enum):
    bit32 = 0
    bit64 = 1


class Compression(Enum):
    none = 0
    zlib = 1


class BinaryDataArray:
    def __init__(self, elem: etree._Element, kind: DataKind, precision: Precision, compression: Compression, data: np.ndarray):
        self.elem = elem
        self.data = data
        self.compression = compression
        self.precision = precision
        self.kind = kind

    @staticmethod
    def from_element(elem: etree._Element) -> 'BinaryDataArray':
        if xpath(elem, 'ns:cvParam[@accession="MS:1000515"]'):
            kind = DataKind.intensity
        elif xpath(elem, 'ns:cvParam[@accession="MS:1000514"]'):
            kind = DataKind.mz
        else:
            raise Exception('no kind cvParam')

        if xpath(elem, 'ns:cvParam[@accession="MS:1000523"]'):
            precision = Precision.bit64
        elif xpath(elem, 'ns:cvParam[@accession="MS:1000521"]'):
            precision = Precision.bit32
        else:
            raise Exception('no precision cvParam')

        if xpath(elem, 'ns:cvParam[@accession="MS:1000576"]'):
            compression = Compression.none
        elif xpath(elem, 'ns:cvParam[@accession="MS:1000574"]'):
            compression = Compression.zlib
        else:
            raise Exception('no compression cvParam')

        data = xpath(elem, 'ns:binary/text()')[0]
        data = base64.b64decode(data)
        if compression == Compression.zlib:
            data = zlib.decompress(data)

        dtype = np.dtype(np.float64 if precision is Precision.bit64 else np.float32).newbyteorder('<')
        data = np.frombuffer(data, dtype=dtype)

        return BinaryDataArray(
            elem=elem,
            kind=kind,
            precision=precision,
            compression=compression,
            data=data,
        )

    def update_data(self, data: np.ndarray):
        self.data = data
        data_bytes = self.data.tobytes()
        if self.compression == Compression.zlib:
            data_bytes = zlib.compress(data_bytes)
        data_bytes = base64.b64encode(data_bytes)

        binary_elem = xpath(self.elem, 'ns:binary')[0]
        binary_elem.text = data_bytes
        self.elem.attrib['encodedLength'] = str(len(data_bytes))

    def __repr__(self):
        return "<BinaryDataArray(kind={kind}, precision={precision}, " \
               "compression={compression}, data={data}...>".format(
            precision=self.precision,
            compression=self.compression,
            kind=self.kind,
            data=self.data[:5]
        )


def filter_scans(mz: BinaryDataArray, intensity: BinaryDataArray, threshold_multiplier: int):
    min_int = intensity.data[intensity.data > 0].min()
    threshold = threshold_multiplier * min_int
    data_mask = intensity.data > threshold
    # mz.update_data(mz.data[data_mask])
    # intensity.update_data(intensity.data[data_mask])
    # mz.update_data(mz.data)
    intensity.update_data(intensity.data - threshold)

    return sum(~data_mask)


def process_file(in_filename: str, out_filename: str, threshold_multiplier: int):
    is_spectrum = False
    size_bytes = os.stat(in_filename).st_size

    with open(out_filename, 'w') as of, open(in_filename, encoding='ascii') as f:
        parser = etree.XMLPullParser(("start", "end"))
        progress = tqdm.tqdm(total=size_bytes)

        total_filtered_peaks = 0
        total_peaks = 0
        for line in f:
            progress.update(len(line))
            parser.feed(line.encode('ascii'))
            for action, elem in parser.read_events():  # type: Tuple[str, etree._Element]
                if elem.tag == '{http://psi.hupo.org/ms/mzml}spectrum':
                    if action == 'start':
                        is_spectrum = True
                    elif action == 'end':
                        is_spectrum = False
                        ms_level = attr(elem, 'ns:cvParam[@accession="MS:1000511"]')

                        if ms_level == '1':
                            binary_data_array_list_elem = xpath(elem, 'ns:binaryDataArrayList')[0]
                            binary_data_arrays_elems = xpath(binary_data_array_list_elem, 'ns:binaryDataArray')

                            bd_arrays = {
                                b.kind: b
                                for b in map(BinaryDataArray.from_element, binary_data_arrays_elems)
                            }
                            total_peaks += int(bd_arrays[DataKind.mz].data.shape[0])
                            total_filtered_peaks += int(filter_scans(bd_arrays[DataKind.mz],
                                                                     bd_arrays[DataKind.intensity],
                                                                     threshold_multiplier=threshold_multiplier))

                            elem.attrib['defaultArrayLength'] = str(int(bd_arrays[DataKind.mz].data.shape[0]))
                        of.write(etree.tostring(elem).decode() + '\n')
                elif not is_spectrum:
                    of.write(line)
            if action == 'end':
                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]  # clean up preceding siblings
        progress.close()

        print("Filtered: {} of {} peaks ({:.2f})".format(total_filtered_peaks,
                                                        total_peaks,
                                                        total_filtered_peaks/total_peaks))
