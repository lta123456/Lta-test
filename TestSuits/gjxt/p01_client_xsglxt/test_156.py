import pytest
class Testcase:

     a = [{'1': '1'},
          {'1': '2'},
          {'1': '3'}]
     @pytest.mark.parametrize('aa', a)
     @pytest.mark.usefixtures('init_client')
     def test_fesf(self, aa):
          print('fewaf {}'.format(aa['1']))
          assert True


