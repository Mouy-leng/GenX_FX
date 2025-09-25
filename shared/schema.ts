import {
  pgTable,
  text,
  varchar,
  timestamp,
  boolean,
  integer,
  primaryKey,
  jsonb,
  real,
  uuid,
} from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";
import { z } from "zod";

// Users table
export const users = pgTable("users", {
  id: uuid("id").defaultRandom().primaryKey(),
  username: varchar("username", { length: 50 }).notNull().unique(),
  email: varchar("email", { length: 255 }).notNull().unique(),
  passwordHash: text("password_hash").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
  lastLogin: timestamp("last_login"),
  isActive: boolean("is_active").default(true).notNull(),
  roles: jsonb("roles").default([]).notNull(), // e.g., ['admin', 'trader']
});

// Trading Accounts table
export const tradingAccounts = pgTable("trading_accounts", {
  id: uuid("id").defaultRandom().primaryKey(),
  userId: uuid("user_id")
    .notNull()
    .references(() => users.id),
  accountNumber: varchar("account_number", { length: 100 }).notNull().unique(),
  broker: varchar("broker", { length: 100 }).notNull(),
  balance: real("balance").default(0).notNull(),
  equity: real("equity").default(0).notNull(),
  currency: varchar("currency", { length: 10 }).default("USD").notNull(),
  leverage: integer("leverage").default(100).notNull(),
  accountType: varchar("account_type", { length: 50 }).default("live").notNull(), // e.g., 'live', 'demo'
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
  isReadOnly: boolean("is_read_only").default(false).notNull(),
});

// Positions table
export const positions = pgTable("positions", {
  id: uuid("id").defaultRandom().primaryKey(),
  accountId: uuid("account_id")
    .notNull()
    .references(() => tradingAccounts.id),
  symbol: varchar("symbol", { length: 20 }).notNull(),
  type: varchar("type", { length: 10 }).notNull(), // 'buy' or 'sell'
  volume: real("volume").notNull(),
  openPrice: real("open_price").notNull(),
  openTime: timestamp("open_time").notNull(),
  closePrice: real("close_price"),
  closeTime: timestamp("close_time"),
  stopLoss: real("stop_loss"),
  takeProfit: real("take_profit"),
  profit: real("profit"),
  swap: real("swap"),
  commission: real("commission"),
  status: varchar("status", { length: 20 }).default("open").notNull(), // 'open', 'closed'
  magicNumber: integer("magic_number"),
  comment: text("comment"),
});

// Notifications table
export const notifications = pgTable("notifications", {
  id: uuid("id").defaultRandom().primaryKey(),
  userId: uuid("user_id")
    .notNull()
    .references(() => users.id),
  message: text("message").notNull(),
  isRead: boolean("is_read").default(false).notNull(),
  type: varchar("type", { length: 50 }).default("info").notNull(), // 'info', 'alert', 'trade'
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// Drizzle relations
export const usersRelations = relations(users, ({ many }) => ({
  tradingAccounts: many(tradingAccounts),
  notifications: many(notifications),
}));

export const tradingAccountsRelations = relations(
  tradingAccounts,
  ({ one, many }) => ({
    user: one(users, {
      fields: [tradingAccounts.userId],
      references: [users.id],
    }),
    positions: many(positions),
  }),
);

export const positionsRelations = relations(positions, ({ one }) => ({
  account: one(tradingAccounts, {
    fields: [positions.accountId],
    references: [tradingAccounts.id],
  }),
}));

export const notificationsRelations = relations(notifications, ({ one }) => ({
  user: one(users, {
    fields: [notifications.userId],
    references: [users.id],
  }),
}));

// Zod schemas for API validation
export const insertUserSchema = z.object({
  username: z.string().min(3).max(50),
  email: z.string().email(),
  password: z.string().min(8),
});

export const insertTradingAccountSchema = z.object({
  userId: z.string().uuid(),
  accountNumber: z.string(),
  broker: z.string(),
  balance: z.number().positive().optional(),
  equity: z.number().positive().optional(),
  currency: z.string().length(3).optional(),
  leverage: z.number().int().positive().optional(),
});
