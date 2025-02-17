using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Data.SqlTypes;
using System.Windows.Markup;
using Microsoft.SqlServer.Server;

public partial class UserDefinedFunctions
{
    [Microsoft.SqlServer.Server.SqlFunction(DataAccess = DataAccessKind.Read)]
    public static SqlDouble CalculateAverageWithoutMinMax(SqlString values)
    {
        if (values.IsNull)
        {
            return SqlDouble.Null;
        }

        string[] stringValues = values.Value.Split(',');

        if (stringValues.Length < 3)
        {
            return SqlDouble.Null;
        }

        double[] numbers = new double[stringValues.Length];

        for (int i = 0; i < stringValues.Length; i++)
        {
            if (!double.TryParse(stringValues[i].Trim(), out numbers[i]))
            {
                return SqlDouble.Null;
            }
        }

        double min = numbers[0], max = numbers[0], sum = 0;
        int count = numbers.Length;

        foreach (double num in numbers)
        {
            if (num < min)
            {
                min = num;
            }

            if (num > max)
            {
                max = num;
            }

            sum += num;
        }

        sum -= (min + max);
        count -= 2; 

        if (count <= 0) return SqlDouble.Null;

        double avg = sum / (numbers.Length - 2);
        return new SqlDouble(avg);
    }
}