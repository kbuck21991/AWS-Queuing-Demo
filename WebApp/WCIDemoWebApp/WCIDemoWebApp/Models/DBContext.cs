﻿using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;

namespace WCIDemoWebApp.Models
{
    public class DBContext
    {
        public string ConnectionString { get; set; }

        public DBContext(string connectionString)
        {
            this.ConnectionString = connectionString;
        }

        private MySqlConnection GetConnection()
        {
            return new MySqlConnection(ConnectionString);
        }
        public List<CoinData> GetCoinData()
        {
            List<CoinData> list = new List<CoinData>();

            using (MySqlConnection conn = GetConnection())
            {
                conn.Open();
                MySqlCommand cmd = new MySqlCommand("select * from wci_coindata", conn);

                using (var reader = cmd.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        list.Add(new CoinData()
                        {
                            Id = Convert.ToInt32(reader["Id"]),
                            Text = reader["Text"].ToString()
                        });
                    }
                }
            }
            return list;
        }
    }
}
