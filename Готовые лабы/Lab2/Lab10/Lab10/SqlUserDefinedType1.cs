using System;
using System.Data;
using System.Data.SqlClient;
using System.Data.SqlTypes;
using System.IO;
using Microsoft.SqlServer.Server;


[Serializable]
[Microsoft.SqlServer.Server.SqlUserDefinedType(Format.UserDefined, IsByteOrdered = true, MaxByteSize = 8000)]
public struct PassportData : INullable, IBinarySerialize
{
    public override string ToString()
    {
        return $"{PassportSeries} {PassportNumber}";
    }

    public bool IsNull
    {
        get
        {
            return _null;
        }
    }

    public static PassportData Null
    {
        get
        {
            PassportData h = new PassportData();
            h._null = true;
            return h;
        }
    }

    public void Read(System.IO.BinaryReader r)
    {
        if (r != null)
        {
            PassportSeries = r.ReadString();
            PassportNumber = r.ReadInt32();
        }
    }

    public void Write(System.IO.BinaryWriter w)
    {
        if (w != null)
        {
            w.Write(PassportSeries);
            w.Write(PassportNumber);
        }
    }

    public static PassportData Parse(SqlString s)
    {
        if (s.IsNull)
            return Null;

        string[] parts = s.Value.Split(' ');

        if (parts.Length != 2)
            throw new ArgumentException("Неверный формат. Используйте: 'Series Number'.");

        PassportData passportData = new PassportData();
        passportData.PassportSeries = parts[0].Trim();
        passportData.PassportNumber = int.Parse(parts[1].Trim());

        return passportData;
    }

    public string PassportSeries { get; set; }
    public int PassportNumber { get; set; }

    private bool _null;
}