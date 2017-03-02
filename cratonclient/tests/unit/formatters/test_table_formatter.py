# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Tests for the pretty-table formatter."""
import mock
import prettytable

from cratonclient import crud
from cratonclient.formatters import table
from cratonclient.tests.unit.formatters import base


class TestTableFormatter(base.FormatterTestCase):
    """Tests for cratonclient.formatters.table.Formatter."""

    def setUp(self):
        """Prepare test case for tests."""
        super(TestTableFormatter, self).setUp()
        self.print_patcher = mock.patch('cratonclient.formatters.table.print')
        self.formatter = table.Formatter(mock.Mock())

    def test_initialization(self):
        """Verify we set up defaults for our PrettyTable formatter."""
        self.assertEqual([], self.formatter.fields)
        self.assertEqual({}, self.formatter.formatters)
        self.assertEqual(0, self.formatter.sortby_index)
        self.assertEqual(set([]), self.formatter.mixed_case_fields)
        self.assertEqual([], self.formatter.field_labels)
        self.assertEqual("Property", self.formatter.dict_property)
        self.assertEqual("Value", self.formatter.dict_value)
        self.assertEqual(0, self.formatter.wrap)

    # Case 0: "Everything" that isn't one of the special cases below
    def test_configure(self):
        """Verify we can configure our formatter.

        There are a few special pieces of logic. For the simpler cases, we can
        just exercise those branches here.
        """
        self.formatter.configure(
            mixed_case_fields=['Foo', 'Bar'],
            dict_property='Field',
            dict_value='Stored Value',
            wrap=72,
            # NOTE(sigmavirus24): This value isn't accurate for formatters
            formatters={'foo': 'bar'},
        )

        self.assertEqual({'Foo', 'Bar'}, self.formatter.mixed_case_fields)
        self.assertEqual('Field', self.formatter.dict_property)
        self.assertEqual('Stored Value', self.formatter.dict_value)
        self.assertEqual(72, self.formatter.wrap)
        self.assertDictEqual({'foo': 'bar'}, self.formatter.formatters)

        # Assert defaults remain unchanged
        self.assertEqual([], self.formatter.fields)
        self.assertEqual([], self.formatter.field_labels)
        self.assertEqual(0, self.formatter.sortby_index)

    # Case 1: Just fields
    def test_configure_fields_only(self):
        """Verify the logic for configuring fields."""
        self.formatter.configure(fields=['id', 'name'])
        self.assertListEqual(['id', 'name'], self.formatter.fields)
        self.assertListEqual(['id', 'name'], self.formatter.field_labels)

    # Case 2: fields + field_labels
    def test_configure_fields_and_field_labels(self):
        """Verify the behaviour for specifying both fields and field_labels.

        When we specify both arguments, we need to ensure they're the same
        length. This demonstrates that we can specify different lists of the
        same length and one won't override the other.
        """
        self.formatter.configure(fields=['id', 'name'],
                                 field_labels=['name', 'id'])
        self.assertListEqual(['id', 'name'], self.formatter.fields)
        self.assertListEqual(['name', 'id'], self.formatter.field_labels)

    # Case 3: fields + field_labels different length
    def test_configure_incongruent_fields_and_field_labels(self):
        """Verify we check the length of fields and field_labels."""
        self.assertRaises(
            ValueError,
            self.formatter.configure,
            fields=['id', 'name', 'extra'],
            field_labels=['id', 'name'],
        )
        self.assertRaises(
            ValueError,
            self.formatter.configure,
            fields=['id', 'name'],
            field_labels=['id', 'name', 'extra'],
        )

    # Case 4: sortby_index is None
    def test_configure_null_sortby_index(self):
        """Verify we can configure sortby_index to be None.

        In this case, the user does not want the table rows sorted.
        """
        self.formatter.configure(sortby_index=None)
        self.assertIsNone(self.formatter.sortby_index)

    # Case 5: sortby_index is an integer
    def test_configure_sortby_index_non_negative_int(self):
        """Verify we can configure sortby_index with an int."""
        self.formatter.configure(
            fields=['id', 'name'],
            sortby_index=1,
        )

        self.assertEqual(1, self.formatter.sortby_index)

    # Case 6: sortby_index is a string of digits
    def test_configure_sortby_index_int_str(self):
        """Verify we can configure sortby_index with a str.

        It makes sense to also allow for strings of integers. This test
        ensures that they come out as integers on the other side.
        """
        self.formatter.configure(
            fields=['id', 'name'],
            sortby_index='1',
        )

        self.assertEqual(1, self.formatter.sortby_index)

    # Case 7: sortby_index is negative
    def test_configure_sortby_index_negative_int(self):
        """Verify we cannot configure sortby_index with a negative value.

        This will verify that we can neither pass negative integers nor
        strings with negative integer values.
        """
        self.assertRaises(
            ValueError,
            self.formatter.configure,
            fields=['id', 'name'],
            sortby_index='-1',
        )
        self.assertRaises(
            ValueError,
            self.formatter.configure,
            fields=['id', 'name'],
            sortby_index='-1',
        )

    # Case 8: sortby_index exceeds length of self.field_labels
    def test_configure_sortby_index_too_large_int(self):
        """Verify we can not use an index larger than the labels."""
        self.assertRaises(
            ValueError,
            self.formatter.configure,
            fields=['id', 'name'],
            sortby_index=3,
        )

    def test_sort_kwargs(self):
        """Verify sort_kwargs relies on sortby_index."""
        self.formatter.field_labels = ['id', 'created_at']
        self.assertDictEqual(
            {
                'sortby': 'id',
                'sort_key': self.formatter.sort_key_func,
            },
            self.formatter.sort_kwargs()
        )

        self.formatter.sortby_index = 1
        self.assertDictEqual(
            {
                'sortby': 'created_at',
                'sort_key': self.formatter.sort_key_func,
            },
            self.formatter.sort_kwargs()
        )

        self.formatter.sortby_index = None
        self.assertDictEqual({}, self.formatter.sort_kwargs())

        self.formatter.sortby_index = 0
        mock_sort_key = mock.Mock()
        self.formatter.sort_key_func = mock_sort_key
        self.assertDictEqual(
            {
                'sortby': 'id',
                'sort_key': mock_sort_key,
            },
            self.formatter.sort_kwargs()
        )

    def test_sort_key_func(self):
        """Verify sort_key_func sorts lists with None and another type."""
        unsorted_list = [
            [2, 2],
            [None, 1],
            [1, 1],
            [2, 1],
        ]
        sorted_list = [
            [None, 1],
            [1, 1],
            [2, 1],
            [2, 2],
        ]
        self.assertEqual(
            sorted_list,
            sorted(unsorted_list, key=self.formatter.sort_key_func)
        )

    def test_build_table(self):
        """Verify that we build our table and auto-align it."""
        table = self.formatter.build_table(['id', 'created_at'])
        self.assertIsInstance(table, prettytable.PrettyTable)
        self.assertDictEqual({'created_at': 'l', 'id': 'l'}, table.align)

    def test_build_table_with_labels(self):
        """Verify we pass along our field labels to our table."""
        with mock.patch('prettytable.PrettyTable') as PrettyTable:
            self.formatter.build_table(['id', 'created_at'])

        PrettyTable.assert_called_once_with(['id', 'created_at'])

    def test_handle_instance(self):
        """Verify our handling of resource instances."""
        resource = crud.Resource(mock.Mock(), self.resource_info())
        self.print_ = self.print_patcher.start()
        mocktable = mock.Mock()
        mocktable.get_string.return_value = ''
        with mock.patch('prettytable.PrettyTable') as PrettyTable:
            PrettyTable.return_value = mocktable
            self.formatter.handle_instance(resource)
        self.print_patcher.stop()

        PrettyTable.assert_called_once_with(["Property", "Value"])
        self.assertListEqual([
            mock.call(['id', 1]),
            mock.call(['name', 'Test Resource']),
        ], mocktable.add_row.call_args_list)
        self.print_.assert_called_once_with('')

    def test_handle_generator(self):
        """Verify how we handle generators of instances."""
        info_list = [self.resource_info(id=i) for i in range(15)]
        self.print_ = self.print_patcher.start()
        mocktable = mock.Mock()
        mocktable.get_string.return_value = ''
        self.formatter.configure(fields=['id', 'Name'])
        with mock.patch('prettytable.PrettyTable') as PrettyTable:
            PrettyTable.return_value = mocktable
            self.formatter.handle_generator(crud.Resource(mock.Mock(), info)
                                            for info in info_list)

        PrettyTable.assert_called_once_with(['id', 'Name'])
        self.assertListEqual(
            [mock.call([i, 'Test Resource']) for i in range(15)],
            mocktable.add_row.call_args_list,
        )
        mocktable.get_string.assert_called_once_with(
            sort_key=self.formatter.sort_key_func, sortby='id'
        )
        self.print_.assert_called_once_with('')
