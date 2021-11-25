# High Level Analyzer
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting

from saleae.data import GraphTimeDelta

DISPLAY_FORMAT_CHOICES = {
    'Hex': 'Hex'
}
class Hla(HighLevelAnalyzer):
   
    #temp_frame = None
    # Settings:
    search_for = StringSetting()
    #search_f = StringSetting()
    search_in_type = ChoicesSetting(label='Display Format', choices=DISPLAY_FORMAT_CHOICES.keys())
    #for_spi_test = ChoicesSetting(['MOSI', 'MISO'])
    prefix = StringSetting(label='Message Prefix (optional)')

    result_types = {
        'dec': {
            'format': '{{data.prefix}}'
        },
    }
    def __init__(self):

        self.print_cnt = 0

        self.search_index = 0
        self.match_start_time = None
        self.match_end_time = None
        



        self.search_len = 0
        self.search_raw = []
        nums = self.search_for.split()
        base = 10
        print(nums)
        if (self.search_in_type == "Hex"):
            base = 16
        for n in nums:
            try:
                self.search_raw.append(int(n,base))
               
            except:

                continue
            self.search_len += 1


    def decode(self, frame: AnalyzerFrame):

        if (frame.type != 'data' and frame.type != 'result'):
            return
        try:
            if (frame.type == 'data'):
                ch = frame.data['data'][0]
        except:
            return



        if self.search_len == 0:
            return



        if ch != self.search_raw[self.search_index]:
            self.search_index = 0
            


        if ch == self.search_raw[self.search_index]:
            frames = []
            if self.search_index == 0:
                self.match_start_time = frame.start_time
            self.search_index = self.search_index + 1
            if self.search_index == self.search_len:
                self.match_end_time = frame.end_time

                char = ''
                for i in range(self.search_len):


                    if (self.search_in_type == "Hex"):

                        char += "%02x " % self.search_raw[i]

                    else:

                        char += chr(self.search_raw[i])



                frames.append(AnalyzerFrame(

                    'dec', self.match_start_time, self.match_end_time, {

                    'prefix':str(self.prefix), 'decoded': char.strip() 

                }))

                self.search_index = 0



            return frames
